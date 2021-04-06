from django import forms
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Submit,
    Row,
    Column,
    Fieldset,
    Field,
    Hidden,
    ButtonHolder,
    HTML,
)
from crispy_forms.bootstrap import FormActions
from schemas.models import *
from django.apps import apps


class DataSchemaForm(forms.Form):

    # upper fields
    name = forms.CharField()
    column_separator = forms.ChoiceField(
        label="Column separator", choices=COLUMN_SEPARATOR_CHOICES
    )
    string_character = forms.ChoiceField(
        label="String character", choices=STRING_CHARACTER_CHOICES
    )

    # i_want_to_add_a_new_column = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        # print("Inside DataSchemaForm Init")
        schema_pk = kwargs.pop("schema_pk")

        subclasses = [
            str(subClass).split(".")[-1][:-2].lower()
            for subClass in SchemaColumn.__subclasses__()
        ]

        column_type_switcher = {
            "integercolumn": INTEGER_CH,
            "fullnamecolumn": FULLNAME_CH,
            "jobcolumn": JOB_CH,
            "companycolumn": COMPANY_CH,
            "phonecolumn": PHONE_CH,
        }

        coulmn_rows = []

        super().__init__(*args, **kwargs)

        if schema_pk:
            schema = DataSchemas.objects.get(pk=schema_pk)
        else:
            # no existing schema primary key passed from the caller,
            # so create new schema and its first column
            # with default parameters
            schema = DataSchemas.objects.create(name="New Schema")
            int1 = IntegerColumn.objects.create(
                name="First Column",
                schema=schema,
                order=1,
                range_low=-20,
                range_high=40,
            )

        self.fields["name"].initial = schema.name
        self.fields["column_separator"].initial = schema.column_separator
        self.fields["string_character"].initial = schema.string_character

        # print(self.fields['name'].initial)
        # print(self.fields['column_separator'].initial)
        # print(self.fields['string_character'].initial)

        schema_columns = schema.schemacolumn_set.all().order_by("order")

        for column in schema_columns:
            column_name_field_name = "col_name_%s" % (column.pk,)
            self.fields[column_name_field_name] = forms.CharField(label="Column name")
            self.fields[column_name_field_name].initial = column.name

            column_order_field_name = "col_order_%s" % (column.pk,)
            self.fields[column_order_field_name] = forms.IntegerField(
                min_value=0, label="Order"
            )
            self.fields[column_order_field_name].initial = column.order

            column_type_field_name = "col_type_%s" % (column.pk,)
            self.fields[column_type_field_name] = forms.ChoiceField(
                label="Column type", choices=COLUMN_TYPE_CHOICES
            )
            for subclass in subclasses:
                if hasattr(column, subclass):
                    self.fields[column_type_field_name].initial = [
                        column_type_switcher.get(subclass)
                    ]
                    break

            delete_btn = "delete_col_%s" % (column.pk,)
            edit_btn = "edit_col_%s" % (column.pk,)

            current_row = Row(
                Column(column_name_field_name, css_class="form-group col-md-4 mb-0"),
                Column(column_type_field_name, css_class="form-group col-md-2 mb-0"),
                Column(column_order_field_name, css_class="form-group col-md-2 mb-0"),
                Column(
                    Submit(delete_btn, "Delete"),
                    css_class="form-group col-md-auto mb-0 needs_manual",
                ),
                Column(
                    Submit(edit_btn, "Edit Details"),
                    css_class="form-group col-md-auto mb-0 needs_manual",
                ),
                css_class="form-row",
            )

            coulmn_rows.append(current_row)

        self.helper = FormHelper()

        submit_form_btn = "submit_form_%s" % (schema.pk,)

        self.helper.layout = Layout(
            Fieldset(
                schema.name,
                Row(
                    Column("name", css_class="form-group col-md-6 mb-0"),
                    Column(
                        Submit(submit_form_btn, "Submit"),
                        css_class="form-group col-md-2 mb-0 needs_manual",
                    ),
                    css_class="form-row",
                ),
                Field("column_separator", css_class="form-group col-md-6 mb-0"),
                Field("string_character", css_class="form-group col-md-6 mb-0"),
            )
        )

        self.helper.layout.append(Fieldset("Schema Column", css_class="fieldsets"))
        for coulmn_row in coulmn_rows:
            # print(coulmn_row)
            self.helper.layout[-1].append(coulmn_row)

        current_row = Row(
            HTML(
                "<hr style='border: 0; clear:both; display:block; width: 96%; background-color:black; height: 1px;'>"
            )
        )
        self.helper.layout.append(current_row)

        # self.helper.layout.append('i_want_to_add_a_new_column')

        self.fields["add_column_name"] = forms.CharField(label="New column name")
        self.fields["add_column_name"].initial = "New column"
        self.fields["add_column_order"] = forms.IntegerField(min_value=0, label="Order")
        self.fields["add_column_order"].initial = schema_columns.last().order + 1
        self.fields["add_column_type"] = forms.ChoiceField(
            label="Column type", choices=COLUMN_TYPE_CHOICES
        )
        current_row = Row(
            Column("add_column_name", css_class="form-group col-md-6 mb-0"),
            Column("add_column_type", css_class="form-group col-md-2 mb-0"),
            Column("add_column_order", css_class="form-group col-md-2 mb-0"),
            css_class="form-row",
        )
        self.helper.layout.append(current_row)

        add_column_btn = "add_column_btn_%s" % (schema.pk,)
        self.helper.layout.append(Submit(add_column_btn, "Add New Column"))

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.views.decorators.http import require_POST
from .forms import DataSchemaForm
from schemas.models import *
from django.http import HttpResponseServerError
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
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
)


class AllSchemasView(ListView):
    model = DataSchemas
    template_name = "all_schemas.html"


@require_POST
def delete_schema(request, pk):
    if request.method:
        query = get_object_or_404(DataSchemas, pk=pk)
        query.delete()
    return redirect("all_schemas")


class SchemaView(TemplateView):
    template_name = "schema_create_update.html"

    subclasses = [
        str(subClass).split(".")[-1][:-2].lower()
        for subClass in SchemaColumn.__subclasses__()
    ]
    # currently, ['integerColumn', 'fullnameColumn', 'jobColumn', 'companyColumn', 'phoneColumn']

    column_type_switcher = {
        "integercolumn": INTEGER_CH,
        "fullnamecolumn": FULLNAME_CH,
        "jobcolumn": JOB_CH,
        "companycolumn": COMPANY_CH,
        "phonecolumn": PHONE_CH,
    }

    def save_schema_columns(self, schema, form):
        # print("Inside save_schema_columns function")
        # print(self.subclasses)
        schema_columns = schema.schemacolumn_set.all()
        for column in schema_columns:
            column_name_field_name = "col_name_%s" % (column.pk,)
            column_order_field_name = "col_order_%s" % (column.pk,)
            column_type_field_name = "col_type_%s" % (column.pk,)

            type_form = form.cleaned_data[column_type_field_name]
            # print(type_form)

            type_changed = False
            for subclass in self.subclasses:
                if hasattr(column, subclass):
                    type_db = self.column_type_switcher.get(subclass)
                    if type_db != type_form:
                        new_class = globals()[type_form]
                        new_column = new_class()
                        new_column.name = form.cleaned_data[column_name_field_name]
                        new_column.order = form.cleaned_data[column_order_field_name]
                        new_column.schema = schema
                        column.delete()
                        new_column.save()
                        type_changed = True
                        break
            if not type_changed:
                column.name = form.cleaned_data[column_name_field_name]
                column.order = form.cleaned_data[column_order_field_name]
                column.save()

    def get_general_column_form(self, model_class, column_pk):
        class ColumnFormGeneral(ModelForm):
            def __init__(self, *args, **kwargs):
                super(ColumnFormGeneral, self).__init__(*args, **kwargs)
                self.helper = FormHelper(self)
                save_chng_btn = "save_schema_columns_chng_btn_%s" % (column_pk,)
                self.helper.layout.append(Submit(save_chng_btn, "Save changes"))

            class Meta:
                model = model_class
                exclude = ["schema", "order"]

        return ColumnFormGeneral

    def process_btn_add_column(self, elem, form_data):
        # print('Add Column button processing')
        self.pk = [int(s) for s in elem.split("_") if s.isdigit()][0]
        form = DataSchemaForm(form_data, schema_pk=self.pk)
        if form.is_valid():
            schema = get_object_or_404(DataSchemas, pk=self.pk)
            new_column_type = form.cleaned_data["add_column_type"]
            new_column = globals()[new_column_type]()
            new_column.name = form.cleaned_data["add_column_name"]
            new_column.order = form.cleaned_data["add_column_order"]
            new_column.schema = schema
            try:
                new_column.save()
            except Exception as err:
                pass
        else:
            return HttpResponseServerError()
        return (self.pk, None)

    def process_btn_delete_column(self, elem, form_data):
        # print('Delete Column button processing')
        column_pk = [int(s) for s in elem.split("_") if s.isdigit()][0]
        self.pk = SchemaColumn.objects.get(pk=column_pk).schema.pk
        SchemaColumn.objects.get(pk=column_pk).delete()
        return (self.pk, None)

    def process_btn_edit_column_details(self, elem, form_data):
        # print('Edit Column details button processing')
        column_pk = [int(s) for s in elem.split("_") if s.isdigit()][0]
        column = get_object_or_404(SchemaColumn, pk=column_pk)
        self.pk = column.schema.pk
        for subclass in self.subclasses:
            if hasattr(column, subclass):
                column_model = apps.get_model("schemas", subclass)
                column = get_object_or_404(column_model, pk=column_pk)

                # from pprint import pprint
                # print()
                # pprint(vars(column))
                # print()
                # print(model_to_dict(column, fields=[field.name for field in column._meta.fields]))

                form_class = self.get_general_column_form(column_model, column_pk)
                form = form_class(
                    initial=model_to_dict(
                        column, fields=[field.name for field in column._meta.fields]
                    )
                )
                break
        return (None, form)

    def process_btn_submit_form(self, elem, form_data):
        # print('Submit Form button processing')
        self.pk = [int(s) for s in elem.split("_") if s.isdigit()][0]
        form = DataSchemaForm(form_data, schema_pk=self.pk)
        if form.is_valid():
            schema = get_object_or_404(DataSchemas, pk=self.pk)
            schema.name = form.cleaned_data["name"]
            schema.column_separator = form.cleaned_data["column_separator"]
            schema.string_character = form.cleaned_data["string_character"]
            schema.save()
            self.save_schema_columns(schema, form)
        else:
            return HttpResponseServerError()
        return (self.pk, None)

    def process_btn_save_chng_column(self, elem, form_data):
        # print('Save Changes in Column button processing')
        column_pk = [int(s) for s in elem.split("_") if s.isdigit()][0]
        column = get_object_or_404(SchemaColumn, pk=column_pk)
        self.pk = column.schema.pk
        for subclass in self.subclasses:
            if hasattr(column, subclass):
                column_model = apps.get_model("schemas", subclass)
                column = get_object_or_404(column_model, pk=column_pk)
                form_class = self.get_general_column_form(column_model, column_pk)
                form = form_class(data=form_data, instance=column)

                # from pprint import pprint
                # print()
                # print('Before form save')
                # pprint(vars(column))
                # print()

                if form.is_valid():
                    form.save()
                else:
                    return (self.pk, form)

                # from pprint import pprint
                # print()
                # print('After form save')
                # pprint(vars(column))
                # print()
        return (self.pk, None)

    btn_functions = {
        "add_new_col": process_btn_add_column,
        "delete_col": process_btn_delete_column,
        "edit_col": process_btn_edit_column_details,
        "submit_form": process_btn_submit_form,
        "save_schema_columns_chng": process_btn_save_chng_column,
    }

    def post(self, request, *args, **kwargs):
        # print()
        # print('Inside SchemaView post')
        # print(request.POST)
        # print()
        # print(self.kwargs)
        # print()
        context = self.get_context_data()
        self.pk = self.kwargs.get("pk", None)
        if self.pk is not None:
            try:
                schema = DataSchemas.objects.get(pk=self.pk)
            except ObjectDoesNotExist:
                return redirect("all_schemas")
        form = None
        btn_pressed = None

        # source of key.startswith idea - https://stackoverflow.com/questions/13101853/select-post-get-parameters-with-regular-expression
        for key in request.POST:
            if key.startswith("delete_col_"):
                btn_pressed = "delete_col"
            if key.startswith("edit_col_"):
                btn_pressed = "edit_col"
            if key.startswith("add_column_btn_"):
                btn_pressed = "add_new_col"
            if key.startswith("submit_form_"):
                btn_pressed = "submit_form"
            if key.startswith("save_schema_columns_chng_btn_"):
                btn_pressed = "save_schema_columns_chng"

            if btn_pressed is not None:
                funt_to_call = self.btn_functions.get(btn_pressed)
                self.pk, form = funt_to_call(self, key, form_data=request.POST)
                break

        # if self.pk:
        # print('We have self.pk')
        # else:
        # print('no self.pk determined, so processing case - create new schema')
        if form is None:
            form = DataSchemaForm(schema_pk=self.pk)
        context["form"] = form
        return super(TemplateView, self).render_to_response({"form": context["form"]})

    def get_context_data(self, **kwargs):
        context = super(SchemaView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        return redirect("all_schemas")

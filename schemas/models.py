from django.db import models
from django.core.validators import RegexValidator

INTEGER_CH = "IntegerColumn"
FULLNAME_CH = "FullNameColumn"
JOB_CH = "JobColumn"
PHONE_CH = "PhoneColumn"
COMPANY_CH = "CompanyColumn"
COLUMN_TYPE_CHOICES = [
    (INTEGER_CH, "Integer"),
    (FULLNAME_CH, "Full Name"),
    (JOB_CH, "Job"),
    (PHONE_CH, "Phone"),
    (COMPANY_CH, "Company"),
]

DOUBLE_QUOTE = '"'
SINGLE_QUOTE = "'"
STRING_CHARACTER_CHOICES = [
    (DOUBLE_QUOTE, 'Double-quote(")'),
    (SINGLE_QUOTE, "Single-quote(')"),
]

COMMA = ","
SEMICOLON = ";"
COLUMN_SEPARATOR_CHOICES = [(COMMA, "Comma(,)"), (SEMICOLON, "Semicolon(;)")]


class DataSchemas(models.Model):

    name = models.CharField(max_length=100)
    column_separator = models.CharField(
        max_length=1,
        choices=COLUMN_SEPARATOR_CHOICES,
        default=COMMA,
    )
    string_character = models.CharField(
        max_length=1,
        choices=STRING_CHARACTER_CHOICES,
        default=DOUBLE_QUOTE,
    )
    modif_date = models.DateField(auto_now=True)

    def get_absolute_url(self):
        return reverse("schema_add_update", args=[str(self.id)])


class SchemaColumn(models.Model):
    name = models.CharField(max_length=100)
    schema = models.ForeignKey(DataSchemas, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        unique_together = [["schema", "name"], ["schema", "order"]]

    def save(self, *args, **kwargs):
        self.validate_unique()
        super(SchemaColumn, self).save(*args, **kwargs)


class IntegerColumn(SchemaColumn):
    range_low = models.IntegerField(blank=True, null=True, default=-20)
    range_high = models.IntegerField(blank=True, null=True, default=40)


class FullNameColumn(SchemaColumn):
    first_name = models.CharField(max_length=10, blank=True, null=True)
    last_name = models.CharField(max_length=15, blank=True, null=True)


class JobColumn(SchemaColumn):
    job_name = models.CharField(max_length=100, blank=True, null=True)


class CompanyColumn(SchemaColumn):
    company_name = models.CharField(max_length=100, blank=True, null=True)


class PhoneColumn(SchemaColumn):
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, blank=True, null=True
    )  # validators should be a list

import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "planeks.settings")
django.setup()
from schemas.models import *

if not DataSchemas.objects.filter(name='Initial Schema Test').exists():
    schema1 = DataSchemas.objects.create(name='Initial Schema Test')
    int1 = IntegerColumn.objects.create(name='int1_range_defaluts', schema=schema1, order=1, range_low=-20,range_high = 40)
    # int2 = IntegerColumn.objects.create(name='int2_range_modified', schema=schema1, order=2, range_low=-14,range_high = 23)
    # int3 = IntegerColumn.objects.create(name='int3', schema=schema1, order=0)
    fn1 = FullNameColumn.objects.create(name='fn1', schema=schema1, order=3)
    jb1 = JobColumn.objects.create(name='jb1', schema=schema1, order=4)
    # fn2 = FullNameColumn.objects.create(name='fn2', schema=schema1, order=5)
    co1 = CompanyColumn.objects.create(name='co1', schema=schema1, order=6)
    phone1 = PhoneColumn.objects.create(name='phone1', schema=schema1, order=7)
    co2 = CompanyColumn.objects.create(name='co2', schema=schema1, order=8)
    # co3 = CompanyColumn.objects.create(name='co3', schema=schema1, order=9)
    int4 = IntegerColumn.objects.create(name='int4', schema=schema1, order=10, range_low=-20,range_high = 40)
    # int5 = IntegerColumn.objects.create(name='int5', schema=schema1, order=11)
    # int6 = IntegerColumn.objects.create(name='int6', schema=schema1, order=12)
    # fn3 = FullNameColumn.objects.create(name='fn3', schema=schema1, order=13)
    # jb2 = JobColumn.objects.create(name='jb2', schema=schema1, order=14)
    # fn4 = FullNameColumn.objects.create(name='fn4', schema=schema1, order=15)
    # co4 = CompanyColumn.objects.create(name='co4', schema=schema1, order=16)
    # phone2 = PhoneColumn.objects.create(name='phone2', schema=schema1, order=17)
    # co5 = CompanyColumn.objects.create(name='co5', schema=schema1, order=18)
    # co6 = CompanyColumn.objects.create(name='co6', schema=schema1, order=19)


# print(schema1.columns_set.all())
# print(Columns.__subclasses__())
# print(Columns.objects.all())
# for column in schema1.columns_set.all():
    # print(column.name)

# exec(open('db_init.py').read())
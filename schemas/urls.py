from django.urls import path
from . import views
from .views import SchemaView, AllSchemasView

urlpatterns = [
path('create_schema/', SchemaView.as_view(), name='schema_create_update'),
path('schema/<int:pk>/', SchemaView.as_view(), name='schema_create_update'),
path('', AllSchemasView.as_view(), name='all_schemas'),
path('delete/<int:pk>/', views.delete_schema, name="delete_schema"),
]
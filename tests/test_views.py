from django.test import TestCase, Client
from django.urls import reverse, resolve
from schemas.views import AllSchemasView, SchemaView
from schemas.models import DataSchemas, SchemaColumn, IntegerColumn, FullNameColumn, JobColumn, CompanyColumn, PhoneColumn
from model_bakery import baker

items_number = 2
column_classes_count = 5
subclasses = [str(subClass).split('.')[-1][:-2].lower() for subClass in SchemaColumn.__subclasses__()]

def createTestData():
    schemas = baker.make('schemas.DataSchemas', _quantity=items_number)
    int_cols = baker.make('schemas.IntegerColumn', schema=schemas[0], _quantity=items_number)
    fullname_cols = baker.make('schemas.FullNameColumn', schema=schemas[0], _quantity=items_number)
    job_cols = baker.make('schemas.JobColumn', schema=schemas[0], _quantity=items_number)
    company_cols = baker.make('schemas.CompanyColumn', schema=schemas[0], _quantity=items_number)
    phone_cols = baker.make('schemas.PhoneColumn', schema=schemas[0], _quantity=items_number)
    return(schemas, int_cols, fullname_cols, job_cols, company_cols, phone_cols)  
    
class AllSchemasViewTests(TestCase):
    
    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.url = reverse('all_schemas')
        self.client = Client()
        self.response = self.client.get(self.url)

    def test_all_schemas_status_code(self):
        self.assertEqual(self.response.status_code, 200)
        
    def test_all_schemas_status_code_post(self):
        self.response_post = self.client.post(self.url)
        self.assertEqual(self.response_post.status_code, 405) # method not allowed
    
    def test_all_schemas_template(self):
        self.assertTemplateUsed(self.response, 'all_schemas.html')

    def test_all_schemas_contains_correct_html(self):
        self.assertContains(self.response, 'Create new schema')
    
    def test_all_schemas_does_not_contain_incorrect_html(self): 
        self.assertNotContains(self.response, 'Hi there! I should not be on the page.')
    
    def test_all_schemas_url_resolves_search_view(self):
        view = resolve('/')
        self.assertEqual(view.func.__name__, 'AllSchemasView')
        
    @classmethod
    def tearDownClass(self):
        super().tearDownClass()
        
class DeleteSchemaViewTests(TestCase):
    
    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.schemas, self.int_cols, self.fullname_cols, self.job_cols, self.company_cols, self.phone_cols = createTestData()
        self.url = reverse('delete_schema', args=[self.schemas[0].pk])
        self.client = Client()
        self.response = self.client.post(self.url, follow = True)
        
    def test_delete_schema_status_code(self):
        self.assertEqual(self.response.status_code, 200)
        
    def test_delete_schema_status_code_get(self):
        self.response_get = self.client.get(self.url)
        self.assertEqual(self.response_get.status_code, 405) # method not allowed
    
    def test_delete_schema_template(self):
        self.assertTemplateUsed(self.response, 'all_schemas.html')

    def test_delete_schema_contains_correct_html(self):
        self.assertContains(self.response, 'Create new schema')
    
    def test_delete_schema_does_not_contain_incorrect_html(self): 
        self.assertNotContains(self.response, 'Hi there! I should not be on the page.')
        
    def test_delete_schema_redirect(self): 
        self.assertRedirects(self.response, '/', status_code=302, 
        target_status_code=200, fetch_redirect_response=True)

    def test_delete_schema_url_resolves(self):
        view = resolve(self.url)
        self.assertEqual(view.func.__name__, 'delete_schema')
        
    @classmethod
    def tearDownClass(self):
        super().tearDownClass()        
        
class SchemaViewTests(TestCase):
    
    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.schemas, self.int_cols, self.fullname_cols, self.job_cols, self.company_cols, self.phone_cols = createTestData()
        self.url = reverse('schema_create_update', args=[self.schemas[0].pk])
        self.client = Client()
        self.response = self.client.post(self.url)        
    
    def test_schema_status_code(self):
        self.assertEqual(self.response.status_code, 200)
            
    def test_schema_template(self):
        self.assertTemplateUsed(self.response, 'schema_create_update.html')

    def test_schema_contains_correct_html(self):
        self.assertContains(self.response, 'Column separator')
        self.assertContains(self.response, 'String character')
        self.assertContains(self.response, 'Schema Column')
        self.assertContains(self.response, 'Column name')
        self.assertContains(self.response, 'Order')
        # self.assertContains(self.response, 'I want to add a new column')
        self.assertContains(self.response, 'New column name')
    
    def test_schema_does_not_contain_incorrect_html(self): 
        self.assertNotContains(self.response, 'Hi there! I should not be on the page.')

    def test_schema_url_resolves(self):
        view = resolve(self.url)
        self.assertEqual(view.func.__name__, 'SchemaView')
    
    @classmethod
    def tearDownClass(self):
        super().tearDownClass()          
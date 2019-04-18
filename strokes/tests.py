from django.test import TestCase

# Create your tests here.
from .models import *

class DocumentTestCase(TestCase):

            
    def setUp(self):
        self.customer = Customer.objects.create(
            name="Test case customer",
            api_key="12345"
            )

        self.document_setting = DocumentSetting.objects.create(
            default_name="Test case default name",
            customer_id = self.customer.id
            )

        self.page_settings = []
        self.last_page_number = 1
        page_one_setting = PageSetting.objects.create(
                document_setting_id=self.document_setting.id,
                number=self.last_page_number,
                width=210,
                height=297,
                customer_id = self.customer.id
                )
        self.page_settings.append(page_one_setting)

        self.document = Document.objects.create(
            name="Test case name",
            identifier="test_case_identifier",
            document_setting_id=self.document_setting.id,
            customer_id = self.customer.id
            )
        
        self.pages = []
        page_one = Page.objects.create(
            page_setting_id=self.page_settings[0].id,
            document_id=self.document.id,
            address="test_case_address",
            number=self.last_page_number,
            customer_id = self.customer.id
            )
        self.pages.append(page_one)
        
        for s in range(2):
            stroke = Stroke.objects.create(
                page_id=self.pages[0].id,
                customer_id = self.customer.id
                )
            for d in range(3):
                dot = Dot.objects.create(
                    stroke_id=stroke.id,
                    x=d,
                    y=s+d,
                    customer_id = self.customer.id
                    )
                
    def test_get_page_strokes_as_json(self):
        page_strokes_json = self.pages[0].get_strokes_as_json()
        #print(page_strokes_json)
        self.assertEqual(self.pages[0].stroke_set.count(), len(page_strokes_json))
        self.assertEqual(self.pages[0].stroke_set.first().dot_set.count(), len(page_strokes_json[0]['dots']))
        self.assertIsInstance(page_strokes_json[0]['dots'][0]['x'], float)

    def test_customer_access_to_others_data(self):
        other_customer = Customer.objects.create(
            name="Other test case customer",
            api_key="12345"
            )

        self.assertEqual(Document.objects.filter(customer_id=other_customer.id).count(), 0)
        self.assertEqual(Page.objects.filter(customer_id=other_customer.id).count(), 0)
        self.assertEqual(Stroke.objects.filter(customer_id=other_customer.id).count(), 0)
        self.assertEqual(Dot.objects.filter(customer_id=other_customer.id).count(), 0)

    def test_save_stroke_by_address(self):
        strokes_json = json.loads('{ "dots": [ { "x": 71, "y": 195 }, { "x": 71, "y": 216.33333 }, { "x": 71, "y": 216.66667 }, { "x": 71, "y": 217 }, { "x": 72.666664, "y": 217 }, { "x": 74, "y": 216.66667 }, { "x": 75.333336, "y": 216.33333 }, { "x": 76.333336, "y": 215 }, { "x": 76.333336, "y": 214.66667 }, { "x": 76.666664, "y": 214.33333 }, { "x": 76.666664, "y": 214 }, { "x": 76.666664, "y": 214 }, { "x": 77.666664, "y": 213 } ]}')

        self.last_page_number += 1
        temp_page = Page.objects.create(
            page_setting_id=self.page_settings[0].id,
            document_id=self.document.id,
            address="test_stroke_case_address",
            number=self.last_page_number,
            customer_id = self.customer.id
            )
        
        Stroke.save_by_address(temp_page.address, strokes_json, self.customer.id)
        self.assertEqual(Stroke.objects.filter(page_id=temp_page.id, customer_id=self.customer.id).count(), 1)

    def test_save_stroke_by_document_page(self):
        strokes_json = json.loads('{ "dots": [ { "x": 71, "y": 180 }, { "x": 71, "y": 183.66667 }, { "x": 71, "y": 187.33333 }, { "x": 71, "y": 195 }, { "x": 71, "y": 216.33333 }, { "x": 71, "y": 216.66667 }, { "x": 71, "y": 217 }, { "x": 72.666664, "y": 217 }, { "x": 74, "y": 216.66667 }, { "x": 75.333336, "y": 216.33333 }, { "x": 76.333336, "y": 215 }, { "x": 76.333336, "y": 214.66667 }, { "x": 77.666664, "y": 213 } ]}')

        self.last_page_number += 1
        temp_page = Page.objects.create(
            page_setting_id=self.page_settings[0].id,
            document_id=self.document.id,
            address="test_stroke_case_address",
            number=self.last_page_number,
            customer_id = self.customer.id
            )
        
        Stroke.save_by_document_page(self.document.identifier, temp_page.number, strokes_json, self.customer.id)
        self.assertEqual(Stroke.objects.filter(page_id=temp_page.id, customer_id=self.customer.id).count(), 1)


    def test_save_page(self):
        self.last_page_number += 1
        page_json = json.loads('{{"number": {0} }}'.format(self.last_page_number))

        temp_page_setting = PageSetting.objects.create(
                document_setting_id=self.document_setting.id,
                number=self.last_page_number,
                width=210,
                height=297,
                customer_id = self.customer.id
                )
                
        Page.save_page(self.customer.id, page_json, "testing-save-page", self.document.identifier)
        Page.save_page(self.customer.id, page_json, "testing-save-page", self.document.identifier)
        self.assertEqual(Page.objects.filter(number=self.last_page_number, customer_id=self.customer.id).count(), 1)

from django.test import TestCase

# Create your tests here.
from .models import *

class DocumentTestCase(TestCase):

    def setUp(self):
        self.customer = Customer.objects.create(
            name="Test case customer",
            token="12345"
            )

        self.document_setting = DocumentSetting.objects.create(
            default_name="Test case default name",
            customer_id = self.customer.id
            )

        self.page_settings = []
        page_one_setting = PageSetting.objects.create(
                document_setting_id=self.document_setting.id,
                number=1,
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
            number=1,
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
        print(page_strokes_json)
        self.assertEqual(self.pages[0].stroke_set.count(), len(page_strokes_json))
        self.assertEqual(self.pages[0].stroke_set.first().dot_set.count(), len(page_strokes_json[0]['dots']))
        self.assertIsInstance(page_strokes_json[0]['dots'][0]['x'], float)

    def test_customer_access_to_others_data(self):
        other_customer = Customer.objects.create(
            name="Other test case customer",
            token="12345"
            )

        self.assertEqual(Document.objects.filter(customer_id=other_customer.id).count(), 0)
        self.assertEqual(Page.objects.filter(customer_id=other_customer.id).count(), 0)
        self.assertEqual(Stroke.objects.filter(customer_id=other_customer.id).count(), 0)
        self.assertEqual(Dot.objects.filter(customer_id=other_customer.id).count(), 0)

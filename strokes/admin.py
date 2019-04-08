from django.contrib import admin

from .models import Customer
from .models import DocumentSetting
from .models import PageSetting
from .models import FieldSetting
from .models import RecognitionSetting
from .models import Document
from .models import Page
from .models import Field
from .models import RecognitionResult
from .models import RecognitionCandidate
from .models import Stroke
from .models import Dot

# Register your models here.
admin.site.register(Customer)
admin.site.register(DocumentSetting)
admin.site.register(PageSetting)
admin.site.register(FieldSetting)
admin.site.register(RecognitionSetting)
admin.site.register(Document)
admin.site.register(Page)
admin.site.register(Field)
admin.site.register(RecognitionResult)
admin.site.register(RecognitionCandidate)
admin.site.register(Stroke)
admin.site.register(Dot)

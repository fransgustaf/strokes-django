from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Document, Page, Stroke, Dot, RecognitionResult, Field
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
import json

from django.utils.safestring import mark_safe

from rest_framework import generics
from .serializers import *

class DocumentList(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


class DocumentDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    lookup_url_kwarg = 'document_pk'


class DocumentPageList(generics.ListCreateAPIView):
    serializer_class = PageSerializer
    
    def get_queryset(self):
        queryset = Page.objects.all()
        document_pk = self.kwargs.get(DocumentDetails.lookup_url_kwarg)
        return Page.objects.filter(document_id=document_pk)


class PageDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PageSerializer
    lookup_url_kwarg = 'page_pk'

    def get_queryset(self):
        page_pk = self.kwargs.get(self.lookup_url_kwarg)
        return Page.objects.filter(id=page_pk)

class PageStrokeList(generics.ListCreateAPIView):
    serializer_class = StrokeSerializer
    lookup_url_kwarg = 'page_pk'

    def get_queryset(self):
        queryset = Page.objects.all()
        page_pk = self.kwargs.get(self.lookup_url_kwarg)
        pages = Page.objects.filter(id=page_pk)
        return Stroke.objects.filter(page_id=page_pk)

class PageFieldList(generics.ListCreateAPIView):
    serializer_class = FieldSerializer
    lookup_url_kwarg = 'page_pk'
    def get_queryset(self):
        page_pk = self.kwargs.get(self.lookup_url_kwarg)
        
        return Field.objects.filter(page_id=page_pk)







def index(request):
    doc_id = request.GET.get('document', '')
    page_number = 1 if request.GET.get('page', '') == '' else request.GET.get('page', '')

    if doc_id:
        document = Document.objects.get(id=doc_id)
    else:
        document = Document.objects.latest('id')
        
    print("document {0} page {1}".format(document.id, page_number))

    page = Page.objects.get(document_id=document.id, number=page_number)
    json_data = {"data": page.get_strokes_as_json()}
    #print(json_data)

    values = []
    
    pages = document.page_set
    address = ''
    for field in page.field_set.all():
        recognition_results = RecognitionResult.objects.filter(field_id=field.id)
        if recognition_results.exists() :
            recognition_candidate = recognition_results.first().recognitioncandidate_set.first()
            # Todo Need to set selected condidate id correctly first, ideally as a nullable foriegn key.
            # recognition_candidate = RecognitionCandidate.objects.get(id=Recognition.objects.get(field_id=field.id).selected_candidate_id)
            values.append(recognition_candidate.value)

    print(values)
    print(address)
    template = loader.get_template('strokes/index.html')
    context = {
        'strokes_data': mark_safe(json.dumps(json_data)),
        'recognition_value': ", ".join(values),
        'address': address,
    }
    return HttpResponse(template.render(context, request))

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Document, Page, Stroke, Dot
from django.core import serializers
import json

from django.utils.safestring import mark_safe

def index(request):
    doc_id = request.GET.get('doc', '')

    if doc_id:
        document = Document.objects.get(id=doc_id)
    else:
        document = Document.objects.latest('id')
        
    print(document)

    strokes_data = []
    for page in document.page_set.all():
        for stroke in page.stroke_set.all():
            stroke_data = []
            for dot in stroke.dot_set.all():
                #stroke.append(serializers.serialize("json", [stroke, ]))
                stroke_data.append({"x": float(dot.x), "y": float(dot.y)})
            strokes_data.append({"dots": stroke_data})

    json_data = {"data": strokes_data}
    #print(json_data)

    values = []
    
    pages = document.page_set
    if pages.exists():
        for field in pages.first().field_set.all():
            recognitions = field.recognition_set
            if recognitions.exists():
                recognition_candidate = recognitions.first().recognitioncandidate_set.first()
                # Todo Need to set selected condidate id correctly first, ideally as a nullable foriegn key.
                # recognition_candidate = RecognitionCandidate.objects.get(id=Recognition.objects.get(field_id=field.id).selected_candidate_id)
                values.append(recognition_candidate.value)

    print(values)
    template = loader.get_template('strokes/index.html')
    context = {
        'strokes_data': mark_safe(json.dumps(json_data)),
        'recognition_value': ", ".join(values),
    }
    return HttpResponse(template.render(context, request))

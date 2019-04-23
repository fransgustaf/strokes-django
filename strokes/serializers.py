from rest_framework import serializers
from .models import *


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'name',
            'identifier',
            'document_setting',
        )
        model = Document


class DotSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'x',
            'y',
        )
        model = Dot

class StrokeSerializer(serializers.ModelSerializer):
    dots = DotSerializer(many=True, read_only=True, source='dot_set')
    class Meta:
        fields = (
            'id',
            'dots',
        )
        model = Stroke


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'page_setting_id',
            'document_id',
            'address',
            'number',
            'background_url',
        )
        model = Page

class RecognitionCandidateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'value',
            'normalized_score',
            'resemblance_score',
        )
        model = RecognitionCandidate

class RecognitionResultSerializer(serializers.ModelSerializer):
    recognition_candidates = RecognitionCandidateSerializer(many=True, read_only=True, source='recognitioncandidate_set')
    class Meta:
        fields = (
            'id',
            'selected_candidate_id',
            'recognition_candidates',
        )
        model = RecognitionResult

class FieldSerializer(serializers.ModelSerializer):
    recognition_results = RecognitionResultSerializer(many=True, read_only=True, source='recognitionresult_set')
    
    class Meta:
        fields = (
            'id',
            'recognition_results',
        )
        model = Field


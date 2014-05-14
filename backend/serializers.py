from rest_framework import serializers

from backend.models import Gloss, ComparisonEntry


class GlossSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gloss
        exclude = ['dictionary']
class ComparisonEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ComparisonEntry
        exclude = ['comparison', 'transcription']

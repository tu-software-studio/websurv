from rest_framework import serializers

from backend.models import Gloss


class GlossSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gloss
        exclude = ['dictionary']

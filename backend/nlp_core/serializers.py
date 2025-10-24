from rest_framework import serializers

class TestSerializer(serializers.Serializer):
    text = serializers.CharField()
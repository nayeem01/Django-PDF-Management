from rest_framework import serializers
from .models import Documents


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = ["id", "title", "user", "file", "uploaded_at"]
        read_only_fields = ["user", "uploaded_at"]

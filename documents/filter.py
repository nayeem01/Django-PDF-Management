from django_filters.rest_framework import FilterSet
from .models import Documents


class DocumentFilter(FilterSet):
    class Meta:
        model = Documents
        fields = {
            "title": ["icontains"],
            "user": ["exact"],
            "uploaded_at": ["date", "gte", "lte"],
        }

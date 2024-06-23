from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    DocumentListCreateView,
    DocumentUpdateView,
    SingleDocumentRetrieveView,
)

urlpatterns = [
    path("docs/", DocumentListCreateView.as_view()),
    path("singleDocument/<int:pk>", SingleDocumentRetrieveView.as_view()),
    path("doc/<int:pk>", DocumentUpdateView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

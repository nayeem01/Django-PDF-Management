from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import DocumentListCreateView, DocumentUpdateView

urlpatterns = [
    path("docs/", DocumentListCreateView.as_view()),
    path("doc/<int:pk>/", DocumentUpdateView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

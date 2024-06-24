from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ExtractMetaView, MergePDFView


urlpatterns = [
    path("extractMeta/<int:pk>", ExtractMetaView.as_view()),
    path("mergePdfs/", MergePDFView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

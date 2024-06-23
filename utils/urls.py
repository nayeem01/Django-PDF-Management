from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ExtractMetaView


urlpatterns = [
    path("extractMeta/<int:pk>", ExtractMetaView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

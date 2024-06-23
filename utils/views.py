from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

import PyPDF2
from django.http import Http404

from documents.permissions import IsOwnerOrReadOnly
from documents.models import Documents
from documents.serializers import DocumetnSerializer


def extract_meta_data(file):
    try:
        read = PyPDF2.PdfReader(file)
        info = read.metadata
        return {
            "author": info.author,
            "creator": info.creator,
            "producer": info.producer,
            "subject": info.subject,
            "title": info.title,
        }
    except Exception as e:
        return {"error": str(e)}


class ExtractMetaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        try:
            document = Documents.objects.get(pk=pk)
            metaData = extract_meta_data(document.file)

            if metaData:
                return Response(metaData, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"message": "no metadata found"}, status=status.HTTP_204_NO_CONTENT
                )
        except Documents.DoesNotExist:  # pylint: disable=no-member
            # return Response(status=status.HTTP_404_NOT_FOUND)
            raise Http404

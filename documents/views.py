from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404


from .models import Documents
from .serializers import DocumetnSerializer


class DocumentListCreateView(APIView):
    """
    List all Documents, or create a new Document.
    """

    def get(self, request):
        documents = Documents.objects.all()
        serializer = DocumetnSerializer(documents, many=True)

        if serializer.data:
            return Response(serializer.data)
        else:
            return Response({"data": []}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = DocumetnSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DocumentUpdateView(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get_object(self, pk):
        try:
            return Documents.objects.get(pk=pk)
        except Documents.DoesNotExist:  # pylint: disable=no-member
            # return Response(status=status.HTTP_404_NOT_FOUND)
            raise Http404

    def get(self, request, pk, format=None):
        document = self.get_object(pk)
        serializer = DocumetnSerializer(document)

        if serializer.data:
            return Response(serializer.data)
        else:
            return Response({"data": []}, status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        document = self.get_object(pk)
        serializer = DocumetnSerializer(document, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        document = self.get_object(pk)
        document.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

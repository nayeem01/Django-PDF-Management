from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend

from .permissions import IsOwnerOrReadOnly
from .models import Documents
from .serializers import DocumentSerializer
from .filter import DocumentFilter


class DocumentListCreateView(generics.ListCreateAPIView):
    """
    List all Documents, or create a new Document.
    """

    permission_classes = [IsAuthenticated]

    queryset = Documents.objects.all()
    # serializer_class = DocumentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DocumentFilter

    def get(self, request):
        documents = self.filter_queryset(self.get_queryset())

        serializer = DocumentSerializer(documents, many=True)

        if serializer.data:
            return Response(serializer.data)
        else:
            return Response({"data": []}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SingleDocumentRetrieveView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            document = Documents.objects.get(pk=pk)
            return document
        except Documents.DoesNotExist:  # pylint: disable=no-member
            # return Response(status=status.HTTP_404_NOT_FOUND)
            raise Http404

    def get(self, request, pk, format=None):
        document = self.get_object(pk)
        serializer = DocumentSerializer(document)

        if serializer.data:
            return Response(serializer.data)
        else:
            return Response({"data": []}, status=status.HTTP_204_NO_CONTENT)


class DocumentUpdateView(APIView):
    """
    Retrieve, update or delete a Document instance.
    """

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            document = Documents.objects.get(pk=pk)
            self.check_object_permissions(self.request, document)
            return document
        except Documents.DoesNotExist:  # pylint: disable=no-member
            # return Response(status=status.HTTP_404_NOT_FOUND)
            raise Http404

    def put(self, request, pk, format=None):
        document = self.get_object(pk)
        serializer = DocumentSerializer(document, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        document = self.get_object(pk)
        document.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

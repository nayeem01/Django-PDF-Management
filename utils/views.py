from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from io import BytesIO
import PyPDF2
from django.http import Http404
from django.http import HttpResponse

from documents.models import Documents


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


def merge_pdfs(docs):
    merger = PyPDF2.PdfWriter()
    for doc in docs:
        pdf_data = doc.file.read()
        reader = PyPDF2.PdfReader(BytesIO(pdf_data))
        merger.append_pages_from_reader(reader)

    merged_pdf = BytesIO()
    merger.write(merged_pdf)
    return merged_pdf.getvalue()


class MergePDFView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            doc_ids = request.query_params.get("doc")

            if not doc_ids:
                return Response(
                    {"error": "doc query param is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            doc_ids = list(map(int, doc_ids.split(",")))

            docs = Documents.objects.filter(pk__in=doc_ids)
            merged_pdf = merge_pdfs(docs)

            response = HttpResponse(merged_pdf, content_type="application/pdf")
            response["Content-Disposition"] = "attachment; filename=merged.pdf"
            return response

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

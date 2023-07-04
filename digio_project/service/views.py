import base64
import json
import logging
import requests
from django.shortcuts import render

from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import DocumentSerializer, DetailsSerializer, GetDocument
from .utils import basic_token, create_response

logger = logging.getLogger(__name__)

base_url = 'https://ext.digio.in:444'


class DocumentView(APIView):

    serializer_class = DocumentSerializer

    def post(self, request, **kwargs):
        """Wrapper for doc upload request."""
        try:
            data = request.data
            serializer = DocumentSerializer(data=data)
            if serializer.is_valid():
                response = self.upload(data)
                return Response(response.json(), status=response.status_code)
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

    def upload(self, data):
        """
        Helper to upload data to final endpoint.
        """
        url = f'{base_url}/v2/client/document/upload'
        payload = {}
        signers = [{
            "name": data.get('name'),
            "identifier": data.get('identifier'),
            "reason": data.get('reason')
        }]
        payload.update({
            'expire_in_days': data.get('expire_in_days'),
            'display_on_page': data.get('display_on_page'),
            'notify_signers': data.get('notify_signers')
        })
        payload['signers'] = signers
        file = data.get('file')
        payload['file_name'] = file.name
        payload['file_data'] = base64.b64encode(file.read())
        files = []
        headers = {
            'Authorization': f'Basic {basic_token()}',
            'content-type': 'application/json'
        }
        response = requests.request("POST",
                                    url,
                                    headers=headers,
                                    data=payload,
                                    files=files)

        return response


class DetailsView(APIView):
    """Get status of uploaded document."""

    serializer_class = GetDocument

    def get(self, request, **kwargs):
        """Wrapper for doc upload request."""

        try:
            doc_id = kwargs.get('doc_id')
            url = f"{base_url}/v2/client/document/{doc_id}"
            payload = {}
            headers = {
                'Authorization': f'Basic {basic_token()}',
            }
            response = requests.request("GET",
                                        url,
                                        headers=headers,
                                        data=payload)

            return Response(response.json(), status=response.status_code)

        except Exception as e:
            logger.error(e)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


class GetDoument(APIView):
    """Get Signed uploaded document."""

    serializer_class = GetDocument

    def get(self, request, **kwargs):
        """Wrapper for doc upload request."""

        try:
            doc_id = kwargs.get('doc_id')
            url = f"{base_url}/v2/client/document/download?document_id={doc_id}"
            # testing purpose
            # url = f"https://www.africau.edu/images/default/sample.pdf"
            # headers = {}
            payload = {}
            headers = {
                'Authorization': f'Basic {basic_token()}',
            }
            response = requests.request("GET",
                                        url,
                                        headers=headers,
                                        data=payload)

            response = create_response(response.content)
            return response

        except Exception as e:
            logger.error(e)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

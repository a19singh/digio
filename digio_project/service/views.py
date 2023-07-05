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
    """
    Document View Class

    Method:
    ------
        post: wrapper for document upload.

    """

    serializer_class = DocumentSerializer

    def post(self, request, **kwargs):
        """
        Wrapper for doc upload request

        Returns
        -------
            response: A HttpResponse Object
        """
        try:
            data = request.data
            serializer = DocumentSerializer(data=data)
            if serializer.is_valid():
                response = self._upload(data)
                return Response(response.json(), status=response.status_code)
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

    def _upload(self, data):
        """
        Helper to upload data to final endpoint.

        Returns
        -------
            response: A RequestResponse Object
        """
        url = f'{base_url}/v2/client/document/upload'
        request = {}
        signers = [{
            "name": data.get('name'),
            "identifier": data.get('identifier'),
            "reason": data.get('reason')
        }]
        request.update({
            'expire_in_days': data.get('expire_in_days'),
            'display_on_page': data.get('display_on_page'),
            'notify_signers': data.get('notify_signers')
        })
        request['signers'] = signers
        payload = {'request': json.dumps(request)}
        file = data.get('file')
        files = [('file', (file.name, file.read(), 'application/pdf'))]
        headers = {
            'Authorization': f'Basic {basic_token()}',
        }
        response = requests.request("POST",
                                    url,
                                    headers=headers,
                                    data=payload,
                                    files=files)

        return response


class DetailsView(APIView):
    """
    Document Detail View.

    Method:
    ------
        get: wrapper to get details of document.

    """

    serializer_class = GetDocument

    def get(self, request, **kwargs):
        """
        Wrapper for doc upload request.

        Returns
        -------
            response: A HttpResponse Object
        """
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
    """
    Get Signed uploaded document.

    Method:
    ------
        get: wrapper for document download.

    """

    serializer_class = GetDocument

    def get(self, request, **kwargs):
        """
        Wrapper for doc upload request.

        Returns
        -------
            response: A HttpResponse Object
        """

        try:
            doc_id = request.GET.get('document_id')
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

            # create a httpresponse for the file
            if response.status_code in range(200, 210):
                response = create_response(response.content)
                return response

            return Response(response.reason, status=response.status_code)

        except Exception as e:
            logger.error(e)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

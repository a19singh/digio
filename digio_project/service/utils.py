import time
import base64
from django.conf import settings
from django.http import HttpResponse
from io import BytesIO
from wsgiref.util import FileWrapper


def basic_token():
    """Generate token from provided creds."""

    userpass = settings.CLIENT_ID + ':' + settings.CLIENT_SECRET
    token = base64.b64encode(userpass.encode()).decode()
    return token


def create_response(data, name=f'{int(time.time())}.pdf'):
    """
    data: bytes_data  
    name: name of document
    """
    response = HttpResponse(data, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; \
        filename={name}'

    return response

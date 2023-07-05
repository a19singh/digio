# Digio Service Wrapper

A Service built on top of digio's service to wrapper the api's

## Getting Started

create a python environment using virtualenv

To install use below command
```
pip install virtualenv
```

Create env using command

```
virtualenv digio
```

To activate the environment use

```
source digio/env/activate
```

Once activated, perform final setup by installing the required packages using command

```
python3 install -r requirements.txt
```

Now we are good to go for running our server, to run the django server on localhost use command

```
cd digio
python3 digio_project/manage.py runserver
```

Now we are good to go for api testing.

- to upload document

POST request: http://127.0.0.1:8000/service/upload

- to get details of document

GET request: http://127.0.0.1:8000/service/get-details/<doc_id>

- to fetch signed document

GET request: http://127.0.0.1:8000/service/download/?document_id=<doc_id>

## Improvements

- Validation for uploaded file
- Oauth Authorization on wrapper methods

from django.urls import path
from . import views

urlpatterns = [
    path('upload', views.DocumentView.as_view()),
    path('get-details/<str:doc_id>', views.DetailsView.as_view()),
    path('download/<str:doc_id>', views.GetDoument.as_view()),
]

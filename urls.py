# docusense/urls.py (app urls)
from django.urls import path
from . import views

app_name = 'docusense'

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_document, name='upload_document'),
    path('document/<int:document_id>/', views.document_detail, name='document_detail'),
    path('chat/', views.chat_with_document, name='chat_with_document'),
    path('toggle-status/<int:document_id>/', views.toggle_document_status, name='toggle_document_status'),
]
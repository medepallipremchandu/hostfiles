from django.urls import path, include
from django.conf import settings
from . import views
from django.conf.urls.static import static
 
urlpatterns = [
         path('', views.index, name ='index'),
         path('about/', views.about, name ='about'),
         path('services/', views.services, name ='services'),
         path('terms/', views.terms, name ='terms'),
         path('privacypolicy/', views.privacypolicy, name ='privacypolicy'),
         path('add_file/', views.add_file, name='add_file'),
         path('file/<uuid:public_url>/', views.file_detail, name='file_detail'),
         path("contact/", views.contact, name="contact"),
         path('success/', views.success, name='success'),
         path('upload/', views.upload_image, name='upload_image'),
         path('image_list/', views.image_list, name='image_list'),
         path('image/<int:image_id>/delete/', views.delete_image, name='delete_image'),
         path('image/<int:image_id>/edit/', views.edit_image, name='edit_image'),
         path('files/<int:file_id>/edit/', views.edit_file, name='edit_file'),
         path('files/<int:file_id>/delete/', views.delete_file, name='delete_file'),
         path('upload_pdf', views.upload_pdf, name='upload_pdf'),
         path('pdf_list', views.pdf_list, name='pdf_list'),    
         path('pdfs/<int:pdf_id>/delete/', views.delete_pdf, name='delete_pdf'),
         path('pdfs/<int:pdf_id>/edit/', views.edit_pdf, name='edit_pdf'),
]
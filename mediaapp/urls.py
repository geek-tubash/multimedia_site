from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.media_list, name='media_list'),
    path('upload/', views.upload_media, name='upload_media'),
    path('edit/<int:pk>/', views.edit_media, name='edit_media'),
    path('delete/<int:pk>/', views.delete_media, name='delete_media'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

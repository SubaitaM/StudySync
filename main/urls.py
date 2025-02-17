from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup, name='signup'),         # Default page (index.html)
    path('upload/', views.upload_doc, name='upload'),  # UploadDoc.html
    path('loading/', views.loading, name='loading'),   # Loading.html
    
    path('', views.list_events, name='list_events'),  # Show all events
    path('edit/<int:event_id>/', views.edit_event, name='edit_event'),
    path('delete/<int:event_id>/', views.delete_event, name='delete_event'),
]


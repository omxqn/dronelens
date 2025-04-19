from django.urls import path
from . import views

urlpatterns = [
    path('', views.file, name='file'),  # Default route
    path('file/', views.file, name='file'),
    path('video/<int:video_id>/', views.video_detail, name='video_detail'),
    path('video/<int:video_id>/trim/', views.trim_video, name='trim_video'),
    path('analyze/', views.analyze, name='analyze'),
    path('download-segment/<int:segment_id>/', views.download_video_segment, name='download_video_segment'),
    path('edit-categories/', views.edit_categories, name='edit_categories'),
    path('delete-category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('export/', views.export, name='export'),
]

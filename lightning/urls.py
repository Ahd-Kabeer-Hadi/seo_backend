
from django.urls import path
from . import views as lightning_views
urlpatterns = [
    # path('magic/', lightning_views.magic, name='lightning'),
    path('transcribe/', lightning_views.Transcribe.as_view(), name='transcribe'),
]

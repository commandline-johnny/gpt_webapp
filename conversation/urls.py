from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.chat_view, name='chat'),
    path('load_session/', views.load_session_view, name='load_session'),
    path('set_api_key/', views.set_api_key, name='set_api_key'),
    path('choose_gpt_model/', views.choose_gpt_model, name='choose_gpt_model'),
    path('new_session/', views.new_session_view, name='new_session'),
]

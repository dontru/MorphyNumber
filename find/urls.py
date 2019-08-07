from django.urls import path

from . import views

urlpatterns = [
    path('<str:player_2>/', views.ResultsView.as_view(), name='results'),
    path('<str:player_1>/<str:player_2>/', views.ResultsView.as_view(), name='results'),
]

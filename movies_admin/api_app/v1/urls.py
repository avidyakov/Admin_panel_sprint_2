from django.urls import path

from .views import Movies, MovieDetail

urlpatterns = [
    path('movies/', Movies.as_view()),
    path('movies/<uuid:pk>/', MovieDetail.as_view()),
]

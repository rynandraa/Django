from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("post/new/", views.PostCreateView.as_view(), name= "post-create"),
    path('post/<slug:slug>/edit/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post-detail'),
]
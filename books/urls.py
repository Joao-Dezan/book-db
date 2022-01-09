from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.list, name='list'),
    path('books/', include([
        path('', views.list, name='list'),
        path('create/', views.create, name='create'),
        path('details/<int:id>/', views.details, name='details'),
        path('delete/<int:id>/', views.delete, name='delete'),
        path('edit/<int:id>/', views.edit, name='edit'),
    ])),
    path('auth/', include([
        path('login/', auth_views.LoginView.as_view(), name='login'),
        path('signup/', views.SignUpView.as_view(), name='signup'),
        path('logout/', views.logout_view, name='logout'),
    ])),
]


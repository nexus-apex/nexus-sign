from django.urls import path
from . import views

urlpatterns = [
    path('', lambda r: views.redirect('/dashboard/')),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('documents/', views.document_list, name='document_list'),
    path('documents/create/', views.document_create, name='document_create'),
    path('documents/<int:pk>/edit/', views.document_edit, name='document_edit'),
    path('documents/<int:pk>/delete/', views.document_delete, name='document_delete'),
    path('signrequests/', views.signrequest_list, name='signrequest_list'),
    path('signrequests/create/', views.signrequest_create, name='signrequest_create'),
    path('signrequests/<int:pk>/edit/', views.signrequest_edit, name='signrequest_edit'),
    path('signrequests/<int:pk>/delete/', views.signrequest_delete, name='signrequest_delete'),
    path('templates/', views.template_list, name='template_list'),
    path('templates/create/', views.template_create, name='template_create'),
    path('templates/<int:pk>/edit/', views.template_edit, name='template_edit'),
    path('templates/<int:pk>/delete/', views.template_delete, name='template_delete'),
    path('settings/', views.settings_view, name='settings'),
    path('api/stats/', views.api_stats, name='api_stats'),
]

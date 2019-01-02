from django.urls import path
from . import views

app_name = 'inicio'
urlpatterns = [
    path('', views.index, name='index'),
    path('test', views.test, name='test'),
    path('test/<fecha>', views.test, name='test'),
    path('sesiones', views.sesiones, name='sesiones'),
    path('sesiones/<id_cliente>', views.sesiones, name='sesiones'),
]
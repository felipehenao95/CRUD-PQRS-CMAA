from django.urls import path, re_path
from django.conf import settings
from django.views.static import serve
from app import views


urlpatterns=[
    path('', views.index, name='index'),
    path('list_dps/', views.list_dps, name='list_dps'),
    path('new_dp/', views.new_dp, name='new_dp'),
    path('mapa/', views.mapa, name='mapa'),
    path('graficos/', views.graficos, name='graficos'),
    path('archivos/<int:programmer_id>/', views.archivos2, name='archivos2'),
    path('proyecciones/<int:programmer_id>/', views.proyecciones, name='proyecciones'),
    path('edit_dp/<int:programmer_id>/', views.edit_dp, name='edit_dp'),
    path('delete_user/<int:programmer_id>/', views.delete_user, name='delete_user'), 
    path('delete_rta/<int:peticionario_id>/<str:name>', views.delete_rta, name='delete_rta'), 
    path('delete_document/<int:peticionario_id>/<str:name>', views.delete_document, name='delete_document'),
    path('signin/', views.signin, name='signin'), 
    path('signout/', views.signout, name='signout'),
    path('upload_dps/', views.upload_dps, name='upload_dps'),
    path('export_dps/', views.export_dps, name='export_dps')
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve,{
        'document_root': settings.MEDIA_ROOT,
    })
]
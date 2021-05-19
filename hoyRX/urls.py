
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from api.views import Login, Logout, hoyRxPost, items

#exportaciones para los templates
from api.views import inicio, crearPedido, regUsuario




#rutas del backend

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include(('api.urls', 'api'))),
    path('generate_token', views.obtain_auth_token),
]



urlpatterns += [
    path('login/', Login.as_view(), name = 'login'),
]


urlpatterns += [
    path('logout/', Logout.as_view()),
]

urlpatterns += [
    path('api/post-list/', hoyRxPost),
]

urlpatterns += [
    path('setItem/', items),
]



#rutas de los templates
urlpatterns += [
    path('', inicio,name='index'),
]


urlpatterns += [
    path('generar-pedido/', crearPedido, name='crearPedido'),
]

urlpatterns += [
    path('registro-usuarios/', regUsuario, name='regUsuario'),
]
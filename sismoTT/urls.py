"""sismoTT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.auth.views import login, logout
from inicio.views import homeInicio,sismoUserInsert,routesView,showMap

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', login, {'template_name':'login.html'},name='login'),
    url(r'^logout/$',logout,{'template_name':'logout.html'},name='logout'),
    url(r'^home/$',homeInicio, name='Inicio'),
    url(r'^registeruser/$',sismoUserInsert,{},name='registeruser'),
    url(r'^wsSISMO/',include('WSsismoTT.urls')),
    url(r'^rutas/$',routesView,name='rutas'),
     url(r'^Rutausuario/$',showMap,name="muestraMapa"),

] 
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)   #ONLY DEVELOPMENT SERVER
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
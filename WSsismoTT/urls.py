from django.conf import settings
from django.conf.urls import include, url
from .views import wsLogin, wsLocationsRegister,wsLogout

urlpatterns = [
    url(r'^wsLogin/$', wsLogin,name='wsLogin'),
    url(r'^wsRegisterLog/$', wsLocationsRegister,name='RegisterLogs'),
    url(r'^wsLogout/$', wsLogout,name='Logout'),
  
] 
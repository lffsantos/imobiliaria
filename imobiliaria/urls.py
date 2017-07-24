from django.conf import settings
from django.conf.urls.static import static
from imobiliaria.core.views import (
    save_imovel, list_imoveis, edit_imovel, delete_imovel,
    do_login)
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^cms/imovel/new/$', save_imovel, name='save_imovel'),
    url(r'^cms/imovel/edit/(?P<id>\d+)', edit_imovel, name='edit_imovel'),
    url(r'^cms/imovel/delete/(?P<id>\d+)', delete_imovel, name='delete_imovel'),
    url(r'^$', list_imoveis, name='list_imoveis'),
    url(r'^login/$', do_login, name='login'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
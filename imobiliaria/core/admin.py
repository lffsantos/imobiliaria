from imobiliaria.core.models import Imovel
from django.contrib import admin
from thumbnails import get_thumbnail


class ImovelModelAdmin(admin.ModelAdmin):
    list_display = ['thumbnail', 'endereco']

    def endereco(self, obj):
        return '<b>Endereço:</b> {} - <b>Bairro:</b> {} - <b>Cidade:</b> {} -<b> UF:</b> {}'.format(obj.end, obj.bairro, obj.cidade, obj.uf)

    endereco.allow_tags = True

    def thumbnail(self, obj):
        img = get_thumbnail(obj.imagem, size="150x150", crop="center")
        return '<img src="{0}"/>'.format(img.url)

    thumbnail.allow_tags = True

    def has_add_permission(self, request):
        return False

    list_display_links = None

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        return super(ImovelModelAdmin, self).change_view(request, object_id,
            form_url, extra_context=extra_context)

admin.site.register(Imovel, ImovelModelAdmin)

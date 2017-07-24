from imobiliaria.core.models import Imovel
from django.test import TestCase
import pycep_correios


class ImovelModelTest(TestCase):

    def test_save(self):
        imovel = Imovel()
        imovel.nome = 'Test'
        imovel.cep = '45608850'
        imovel.imagem = 'http://hbn.link/hb-pic'
        imovel.save()
        end_completo = pycep_correios.consultar_cep(imovel.cep)
        assert imovel.end == end_completo['end'] and imovel.uf == end_completo['uf'] and \
               imovel.bairro == end_completo['bairro'] and imovel.cidade == end_completo['cidade']
        self.assertTrue(Imovel.objects.exists())

from django.db import models
import pycep_correios


class Imovel(models.Model):
    nome = models.CharField('nome', max_length=255)
    descricao = models.TextField('descrição', blank=True)
    imagem = models.URLField('imagem')
    bairro = models.CharField('bairro', max_length=255)
    cep = models.CharField('cep', max_length=8)
    cidade = models.CharField('cidade', max_length=255)
    end = models.CharField('end', max_length=255)
    uf = models.CharField('uf', max_length=2)
    valor = models.FloatField('valor', default=0, blank=True)

    class Meta:
        verbose_name = 'imovel'
        verbose_name_plural = 'imoveis'

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        end_completo = pycep_correios.consultar_cep(self.cep)
        self.bairro, self.end = end_completo['bairro'], end_completo['end']
        self.cidade, self.uf = end_completo['cidade'], end_completo['uf']
        super(Imovel, self).save(*args, **kwargs)




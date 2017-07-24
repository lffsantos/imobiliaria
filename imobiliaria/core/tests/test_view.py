from django.contrib.auth.models import User
from os import path
from django.shortcuts import resolve_url as r
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from model_mommy import mommy

from imobiliaria.core.models import Imovel

root = path.abspath(path.join(path.dirname(__file__)))


class ImovelPostValidSave(TestCase):
    def setUp(self):
        img = open(root + '/casa.jpg', 'rb')
        uploaded = SimpleUploadedFile(img.name, img.read())
        data = dict(nome="casa x", cep="45608850",
                    descricao="casa para alugar na praia",
                    valor="100", imagem=uploaded)

        user = User.objects.create_user(username='user', email='user@example.com', password='xxxx')
        self.logged_in = self.client.login(username=user.username, password='xxxx')
        self.resp = self.client.post(r('save_imovel'), data)

    def test_save_imovel(self):
        msg = self.resp.context['msg']['sucesso']
        self.assertContains(self.resp, msg)
        self.assertTrue(Imovel.objects.exists())


class ImovelPostInValidSave(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='user', email='user@example.com', password='xxxx')
        self.logged_in = self.client.login(username=user.username, password='xxxx')
        img = open(root + '/casa.jpg', 'rb')
        self.uploaded = SimpleUploadedFile(img.name, img.read())
        self.data = dict(
            nome="casa x", cep="4560-8850", descricao="casa para alugar na praia",
            valor="100", imagem=self.uploaded
        )

    def test_save_invalid_cep(self):
        data = dict(self.data)
        data['cep'] = "4560-8850"
        self.resp = self.client.post(r('save_imovel'), data)
        msg = self.resp.context['msg']['error']
        self.assertContains(self.resp, msg)
        self.assertFalse(Imovel.objects.exists())

    def test_save_invalid_valor(self):
        data = dict(self.data)
        data['valor'] = 'aaa'
        self.resp = self.client.post(r('save_imovel'), data)
        msg = self.resp.context['msg']['error']
        self.assertContains(self.resp, msg)
        self.assertFalse(Imovel.objects.exists())

    def test_save_no_image(self):
        data = dict(self.data)
        data.pop('imagem')
        self.resp = self.client.post(r('save_imovel'), data)
        msg = self.resp.context['msg']['error']
        self.assertContains(self.resp, msg)
        self.assertFalse(Imovel.objects.exists())


class ImovelPostValidEdit(TestCase):
    def setUp(self):
        img = open(root + '/casa.jpg', 'rb')
        uploaded = SimpleUploadedFile(img.name, img.read())
        self.data = dict(nome="casa x", cep="45608850",
                    descricao="casa para alugar na praia",
                    valor="100", imagem=uploaded)

        user = User.objects.create_user(username='user', email='user@example.com', password='xxxx')
        self.logged_in = self.client.login(username=user.username, password='xxxx')
        self.resp = self.client.post(r('save_imovel'), self.data)

    def test_edit(self):
        imovel = Imovel.objects.all()[0]
        data = dict(self.data)
        data['nome'] = "mudei o nome"
        self.resp = self.client.post(r('edit_imovel', imovel.pk), data)
        msg = self.resp.context['msg']['sucesso']
        self.assertContains(self.resp, msg)
        imovel = Imovel.objects.get(pk=imovel.pk)
        self.assertTrue(imovel.nome, data['nome'])


class ImovelPostInValidEdit(TestCase):
    def setUp(self):
        img = open(root + '/casa.jpg', 'rb')
        uploaded = SimpleUploadedFile(img.name, img.read())
        self.data = dict(nome="casa x", cep="45608850",
                         descricao="casa para alugar na praia",
                         valor="100", imagem=uploaded)

        user = User.objects.create_user(username='user', email='user@example.com', password='xxxx')
        self.logged_in = self.client.login(username=user.username, password='xxxx')
        self.resp = self.client.post(r('save_imovel'), self.data)

    def test_edit(self):
        imovel = Imovel.objects.all()[0]
        data = dict(self.data)
        data['nome'] = ""
        self.resp = self.client.post(r('edit_imovel', imovel.pk), data)
        msg = self.resp.context['msg']['error']
        self.assertContains(self.resp, msg)
        imovel = Imovel.objects.get(pk=imovel.pk)
        self.assertTrue(imovel.nome, self.data['nome'])


class ImovelList(TestCase):
    def setUp(self):
        img = open(root + '/casa.jpg', 'rb')
        uploaded = SimpleUploadedFile(img.name, img.read())
        data = dict(nome="casa x", cep="45608850",
                    descricao="casa para alugar na praia",
                    valor="100", imagem=uploaded)

        user = User.objects.create_user(username='user', email='user@example.com', password='xxxx')
        self.logged_in = self.client.login(username=user.username, password='xxxx')
        self.resp = self.client.post(r('save_imovel'), data)

    def test_list(self):
        self.resp = self.client.get(r('list_imoveis'))
        self.assertContains(self.resp, 'Caminho Quatro')
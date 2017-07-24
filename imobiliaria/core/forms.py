import os
from django.forms import ModelForm

import boto3
from decouple import config
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from imobiliaria.core.models import Imovel
from pycep_correios import CEPInvalido


root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))


class ImovelForm(ModelForm):
    class Meta:
        model = Imovel
        fields = '__all__'

    def is_valid(self):
        cep = self.data.get('cep', '')
        if cep == '' or len(cep) != 8 or not cep.isnumeric():
            raise ValidationError('Informe um CEP válido.')
        if not self.files.get('imagem') and not self.instance.pk:
            raise ValidationError('Adicione uma Imagem ao Anuncio')
        if self.data.get('nome', '') == '':
            raise ValidationError('Informe um Nome para o Anuncio')

        return True

    def clean(self):
        if self.data.get('valor', '') != '':
            try:
                float(self.data.get('valor'))
            except:
                raise ValidationError('Valor informado inválido!')

        return self.cleaned_data

    def save(self):
        if self.instance.pk:
            imovel = self.instance
        else:
            imovel = Imovel()

        imovel.cep = self.data['cep']
        imovel.nome = self.data['nome']
        imovel.descricao = self.data['descricao']
        imovel.valor = float(self.data.get('valor'))
        if self.files.get('imagem'):
            myfile = self.files['imagem']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            filepath = root+'/media/'+filename
            aws_link = upload_image_to_s3(filepath)
            imovel.imagem = aws_link
            os.remove(filepath)
        try:
            imovel.save()
        except CEPInvalido:
            raise ValidationError('Cep Inválido')


def upload_image_to_s3(filename):
    client = boto3.client('s3', aws_access_key_id=config('AWS_ACCESS_KEY_ID'), aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'))
    try:
        client.upload_file(
            filename, config('AWS_BUCKET'), filename.split('/')[-1]
        )
        aws_file_link = "https://s3.amazonaws.com/{bucket}/{filename}".format(
            bucket=config('AWS_BUCKET'),
            filename=filename.split('/')[-1])

        return aws_file_link
    except:
        raise
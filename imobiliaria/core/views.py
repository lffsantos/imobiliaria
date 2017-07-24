import copy

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth.decorators import login_required

from imobiliaria.core.forms import ImovelForm
from imobiliaria.core.models import Imovel


def do_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('save_imovel')

    return render(request, 'core/login.html')


@login_required(login_url='/login/')
def save_imovel(request):
    context = {}
    if request.method == 'POST':
        form = ImovelForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                form.save()
                msg = {"sucesso": "Cadastro Realizado com Sucesso"}
        except ValidationError as exc:
            msg = {'error': exc.message}
        context['msg'] = msg
    return render(request, 'core/cadastro.html', context)


@login_required(login_url='/login/')
def edit_imovel(request, id):
    msg = {}
    try:
        imovel = Imovel.objects.get(pk=id)
        if request.method == 'POST':
            form = ImovelForm(request.POST, request.FILES, instance=imovel)
            if form.is_valid():
                form.save()
                msg = {"sucesso": "Edição Realizada com Sucesso"}
    except ObjectDoesNotExist:
        return render(request, '404.html')
    except ValidationError as exc:
        msg = {'error': exc.message}

    context = {
        'imovel': imovel,
        'msg': msg
    }

    return render(request, 'core/detail.html', context)


@login_required(login_url='/login/')
def delete_imovel(request, id):
    if request.method == 'POST':
        imovel = Imovel.objects.get(id=id)
        imovel.delete()

    return redirect('listagem')


def list_imoveis(request):
    params = {}
    if request.method == 'POST':
        payload = request.POST
        params = copy.copy(payload)
        params.pop('csrfmiddlewaretoken')

    imoveis = Imovel.objects.filter(**params)
    ufs = set(Imovel.objects.order_by('uf').values_list('uf', flat=True))
    cidades = set(Imovel.objects.order_by('cidade').values_list('cidade', flat=True))
    bairros = set(Imovel.objects.order_by('bairro').values_list('bairro', flat=True))
    context = {
        'imoveis': imoveis,
        'ufs': set(ufs),
        'cidades': set(cidades),
        'bairros': set(bairros),
    }
    filters = {}
    for p in params.keys():
        filters.update({p.replace('__in', ''): request.POST.getlist(p)})

    context['filters'] = filters

    return render(request, 'core/list_imoveis.html', context)


@login_required(login_url='/login/')
def listagem(request):
    imoveis = Imovel.objects.all()
    return render(request, 'core/listagem.html', {'imoveis': imoveis})
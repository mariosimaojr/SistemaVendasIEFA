import json
import re
import urllib.error
import urllib.request

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.db.models import CharField, Q, Sum
from django.db.models.functions import Cast, Coalesce
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from apps.movimentacoes_estoque.models import MovimentacaoEstoque

from .models import Produto
from .forms import ProdutoForm


def _montar_prompt_nome_etiqueta(descricao):

    placeholder = '[COLE AQUI O NOME COMPLETO DO PRODUTO]'
    prompt_base = settings.GEMINI_LABEL_PROMPT

    if placeholder in prompt_base:
        return prompt_base.replace(placeholder, descricao)

    return f'{prompt_base}\n{descricao}'


def _limpar_nome_etiqueta(nome):

    nome = re.sub(r'\s+', ' ', nome).strip()
    nome = nome.strip('"\'“”‘’')

    return nome[:25]


def _extrair_texto_gemini(dados):

    candidatos = dados.get('candidates') or []

    if not candidatos:
        return ''

    partes = candidatos[0].get('content', {}).get('parts') or []
    textos = [
        parte.get('text', '')
        for parte in partes
        if parte.get('text')
    ]

    return ' '.join(textos)


def lista(request):

    q = request.GET.get('q', '').strip()

    produtos = Produto.objects.select_related('categoria').annotate(
        sequencia_texto=Cast(
            'sequencia',
            output_field=CharField()
        ),
        estoque_atual=Coalesce(
            Sum('movimentacaoestoque__quantidade'),
            0
        )
    )

    if q:
        filtros = (
            Q(sequencia_texto__icontains=q) |
            Q(nome__icontains=q) |
            Q(descricao__icontains=q) |
            Q(categoria__nome__icontains=q) |
            Q(categoria__descricao__icontains=q)
        )

        if q.isdigit():
            filtros |= Q(sequencia=int(q))

        produtos = produtos.filter(filtros)

    return render(
        request,
        'produtos/lista.html',
        {
            'produtos': produtos,
            'q': q
        }
    )


@require_POST
def sugerir_nome_etiqueta(request):

    if not settings.GEMINI_API_KEY:
        return JsonResponse(
            {'erro': 'A chave da API Gemini não foi configurada.'},
            status=503
        )

    try:
        dados = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse(
            {'erro': 'Requisição inválida.'},
            status=400
        )

    descricao = (dados.get('descricao') or '').strip()

    if not descricao:
        return JsonResponse(
            {'erro': 'Informe a descrição do produto antes de usar a IA.'},
            status=400
        )

    modelo = settings.GEMINI_MODEL.strip()
    modelo_path = modelo if modelo.startswith('models/') else f'models/{modelo}'
    url = f'https://generativelanguage.googleapis.com/v1beta/{modelo_path}:generateContent'

    payload = {
        'contents': [
            {
                'role': 'user',
                'parts': [
                    {
                        'text': _montar_prompt_nome_etiqueta(descricao)
                    }
                ]
            }
        ],
        'generationConfig': {
            'temperature': 0.2,
            'maxOutputTokens': 32
        }
    }

    requisicao = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'Content-Type': 'application/json',
            'x-goog-api-key': settings.GEMINI_API_KEY
        },
        method='POST'
    )

    try:
        with urllib.request.urlopen(requisicao, timeout=30) as resposta:
            resposta_json = resposta.read().decode('utf-8')
    except urllib.error.HTTPError as erro:
        mensagem = 'Não foi possível gerar a sugestão com a IA.'

        try:
            erro_json = json.loads(erro.read().decode('utf-8'))
            mensagem = erro_json.get('error', {}).get('message') or mensagem
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass

        return JsonResponse(
            {'erro': mensagem},
            status=502
        )
    except (TimeoutError, urllib.error.URLError):
        return JsonResponse(
            {'erro': 'A API Gemini não respondeu. Tente novamente.'},
            status=504
        )

    try:
        dados_resposta = json.loads(resposta_json)
    except json.JSONDecodeError:
        return JsonResponse(
            {'erro': 'A API Gemini retornou uma resposta inválida.'},
            status=502
        )

    nome = _limpar_nome_etiqueta(_extrair_texto_gemini(dados_resposta))

    if not nome:
        return JsonResponse(
            {'erro': 'A API Gemini não retornou uma sugestão.'},
            status=502
        )

    return JsonResponse({'nome': nome})


def criar(request):

    produto_criado = request.GET.get('produto_criado')
    quantidade_etiquetas = request.GET.get('quantidade_etiquetas') or 1

    if request.method == 'POST':

        form = ProdutoForm(
            request.POST,
            is_create=True
        )

        if form.is_valid():

            estoque_inicial = form.cleaned_data['estoque_inicial']
            quantidade_etiquetas = max(estoque_inicial, 1)

            with transaction.atomic():

                produto = form.save(commit=False)
                produto.data_cadastro = timezone.now()
                produto.save()

                if estoque_inicial > 0:
                    MovimentacaoEstoque.objects.create(
                        produto=produto,
                        quantidade=estoque_inicial,
                        data_movimento=timezone.now(),
                        observacao='Estoque inicial informado no cadastro do produto.',
                        usuario=request.usuario_logado,
                        tipo_movimento='ENTRADA'
                    )

            return redirect(
                (
                    f"{reverse('produtos:novo')}"
                    f"?produto_criado={produto.sequencia}"
                    f"&quantidade_etiquetas={quantidade_etiquetas}"
                )
            )

    else:

        form = ProdutoForm(
            is_create=True
        )

    return render(
        request,
        'produtos/form.html',
        {
            'form': form,
            'titulo': 'Novo Produto',
            'produto_criado': produto_criado,
            'quantidade_etiquetas': quantidade_etiquetas
        }
    )


def editar(request, pk):

    produto = get_object_or_404(
        Produto,
        pk=pk
    )

    if request.method == 'POST':

        form = ProdutoForm(
            request.POST,
            instance=produto
        )

        if form.is_valid():

            produto = form.save(commit=False)

            if not produto.data_cadastro:
                produto.data_cadastro = timezone.now()

            produto.save()

            return redirect('produtos:lista')

    else:

        form = ProdutoForm(
            instance=produto
        )

    return render(
        request,
        'produtos/form.html',
        {
            'form': form,
            'titulo': 'Editar Produto'
        }
    )


def excluir(request, pk):

    produto = get_object_or_404(
        Produto,
        pk=pk
    )

    produto.delete()

    return redirect('produtos:lista')

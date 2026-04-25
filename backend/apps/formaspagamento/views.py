from django.shortcuts import render, redirect, get_object_or_404
from .models import FormaPagamento
from .forms import FormaPagamentoForm


def lista(request):

    formas = FormaPagamento.objects.all()

    return render(
        request,
        'formaspagamento/lista.html',
        {
            'formas': formas
        }
    )


def criar(request):

    if request.method == 'POST':

        form = FormaPagamentoForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('formaspagamento:lista')

    else:
        form = FormaPagamentoForm()

    return render(
        request,
        'formaspagamento/form.html',
        {
            'form': form,
            'titulo': 'Nova Forma de Pagamento'
        }
    )


def editar(request, pk):

    forma = get_object_or_404(
        FormaPagamento,
        pk=pk
    )

    if request.method == 'POST':

        form = FormaPagamentoForm(
            request.POST,
            instance=forma
        )

        if form.is_valid():
            form.save()
            return redirect('formaspagamento:lista')

    else:
        form = FormaPagamentoForm(
            instance=forma
        )

    return render(
        request,
        'formaspagamento/form.html',
        {
            'form': form,
            'titulo': 'Editar Forma de Pagamento'
        }
    )


def excluir(request, pk):

    forma = get_object_or_404(
        FormaPagamento,
        pk=pk
    )

    forma.delete()

    return redirect('formaspagamento:lista')
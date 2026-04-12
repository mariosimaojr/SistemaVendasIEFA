from django.shortcuts import render, redirect, get_object_or_404

from .models import formaspagamento

from .forms import formaspagamentoForm


def lista(request):

    formas = formaspagamento.objects.all()

    return render(

        request,

        'formaspagamento/lista.html',

        {

            'formas': formas

        }

    )


def criar(request):

    if request.method == 'POST':

        form = formaspagamentoForm(

            request.POST

        )

        if form.is_valid():

            form.save()

            return redirect('formaspagamento:lista')

    else:

        form = formaspagamentoForm()

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

        formaspagamento,

        pk=pk

    )

    if request.method == 'POST':

        form = formaspagamentoForm(

            request.POST,

            instance=forma

        )

        if form.is_valid():

            form.save()

            return redirect('formaspagamento:lista')

    else:

        form = formaspagamentoForm(

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

        formaspagamento,

        pk=pk

    )

    if request.method == 'POST':

        forma.delete()

        return redirect('formaspagamento:lista')

    return render(

        request,

        'formaspagamento/excluir.html',

        {

            'forma': forma

        }

    )
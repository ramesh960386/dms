from django.template import RequestContext, Template
import os
import csv
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.conf import settings as se
from .models import DocumentModel, DocumentType
from .forms import DocumentForm


def csv_data(request, mode):
    # data = {key: value for key, value in request.META.items()}
    # data = [dict(key=value) for key, value in request.META.items()]
    if mode == 'open':
        with open('dict.csv', 'w') as csv_file:
            writer = csv.writer(csv_file)
            # [writer.writerow([key, value]) for key, value in request.META.items()]
            for key, value in request.META.items():
                writer.writerow([key, value])
    else:
        with open('dict.csv') as csv_file:
            reader = csv.reader(csv_file)
            mydict = dict(reader)


def aws(request):
    return render(request, 'aws.html')


def index(request):
    context = {
        'data': DocumentType.objects.all()
    }
    return render(request, 'index.html', context)


class DocumentListView(generic.ListView):
    template_name = 'home.html'
    # model = DocumentModel
    # queryset = DocumentModel.objects.all()
    context_object_name = 'documents'
    # paginate_by = 10
    # ordering = ['-created']

    def get_queryset(self):
        return DocumentModel.objects.filter(doc_type=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(DocumentListView, self).get_context_data(**kwargs)
        context['form'] = DocumentForm(initial={'doc_type': self.kwargs['pk']})
        return context


class DocumentDetailView(generic.DetailView):
    model = DocumentModel
    template_name = 'detail.html'
    context_object_name = 'document'


def is_ajax(self):
    return self.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"


# class BookCreateView(generic.CreateView):
#     # def get(self, request, *args, **kwargs):
#     #     context = {'form': DocumentForm()}
#     #     return render(request, 'books/book-create.html', context)

#     def post(self, request, *args, **kwargs):
#         form = BookCreateForm(request.POST)
#         if form.is_valid():
#             book = form.save()
#             book.save()
#             return HttpResponseRedirect(reverse_lazy('books:detail', args=[book.id]))
#         return render(request, 'books/book-create.html', {'form': form})

def drf_template(request):
    context = {
        'data': DocumentType.objects.all()
    }
    return render(request, 'drf_index.html', context)


#################################################################


def ip_address_processor(request):
    return {'ip_address': request.META['REMOTE_ADDR']}


def client_ip_view(request):
    template = Template('{{ title }}: {{ ip_address }}')
    context = RequestContext(request, {
        'title': 'Your IP Address',
    }, [ip_address_processor])
    return HttpResponse(template.render(context))
#################################################################


def upload(request, id):
    # request.session['temp_data'] = form.cleaned_data
    if request.method == 'POST':
        upload = DocumentForm(request.POST, request.FILES)
        if upload.is_valid():
            upload.save()
            return HttpResponseRedirect(reverse('home', args=[id]))
            # return redirect('home')
            # return reverse_lazy('home', kwargs={'pk': id})
            # HttpResponseRedirect(reverse_lazy('abcfirst', args={'cid': 1}))
            # return redirect('home', pk=id)
        return HttpResponseRedirect(reverse('home', args=[id]))
    return HttpResponseRedirect(reverse('home', args=[id]))


def delete(request, id):
    print(request.path_info)
    data = get_object_or_404(DocumentModel, id=id)
    data.delete()
    # return HttpResponseRedirect(request.path_info)
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

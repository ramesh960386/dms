import os
import csv
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
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
        context['form'] = DocumentForm()
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

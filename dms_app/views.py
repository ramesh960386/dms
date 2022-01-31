import os
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.conf import settings as se
from .models import DocumentModel, DocumentType
from .forms import DocumentForm
from django.contrib.auth.models import User


@login_required(login_url="/login/")
def index(request):
    context = {
        'data': DocumentType.objects.all()
    }
    # context = {'segment': 'index'}
    return render(request, 'dms/dms-categories.html', context)


class DocumentListView(ListView):
    template_name = 'dms/document-list.html'
    # model = DocumentModel
    # queryset = DocumentModel.objects.all()
    context_object_name = 'documents'
    # paginate_by = 10
    # ordering = ['-created']

    def get_queryset(self):
        return DocumentModel.objects.filter(doc_type=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        # context = super(DocumentListView, self).get_context_data(**kwargs)
        context = super().get_context_data(**kwargs)
        context['form'] = DocumentForm(initial={'doc_type': self.kwargs['pk']})
        return context


class DocumentAddFormView(CreateView):
    template_name = 'dms/document-add.html'
    # model = DocumentModel
    # fields = ['name']
    form_class = DocumentForm
    # success_url = reverse_lazy('dms:contact-us')
    # success_url = reverse_lazy('somewhere')
    # success_url = '/dms/'

    def get_initial(self):
        initial = super(DocumentAddFormView, self).get_initial()
        initial.update({'doc_type': self.kwargs['pk']})
        return initial

    def form_valid(self, form):
        fm = form.instance
        fm.doc_owner = fm.created_by = fm.modified_by = self.request.user
        # form.instance.doc_owner = self.request.user
        # form.instance.created_by = self.request.user
        # form.instance.modified_by = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse('dms:myhome', kwargs={'pk': self.kwargs['pk']})


class DocumentUpdateView(UpdateView):
    model = DocumentModel
    # fields = ('id', 'doc_name', 'doc_type', 'doc_owner', 'doc_dept', 'description', 'document',
    #                 'comment', )
    template_name = 'dms/document-add.html'
    form_class = DocumentForm

    def get_success_url(self):
        # print('wow: ', self.request.resolver_match)
        # print('myform: ', self.get_form_kwargs())
        # print('myform: ', self.object.doc_type.pk)
        # return reverse_lazy('dms:myhome', kwargs={'pk': self.object.pk})
        return reverse_lazy('dms:myhome', kwargs={'pk': self.object.doc_type.pk})


class DocumentDeleteView(DeleteView):
    model = DocumentModel

    def get_success_url(self):
        return reverse_lazy('dms:myhome', kwargs={'pk': self.object.doc_type.pk})


class DocumentDetailView(DetailView):
    model = DocumentModel
    template_name = 'dms/document-detail.html'
    context_object_name = 'document'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['now'] = timezone.now()
    #     return context


def upload(request, id):
    # request.session['temp_data'] = form.cleaned_data
    if request.method == 'POST':
        # data = request.POST.dict()
        # user_obj = User.objects.get(pk=request.user.pk)
        # data['created_by'] = data['modified_by'] = user_obj
        # data['user'] = request.user
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            fm = form.instance
            fm.doc_owner = fm.created_by = fm.modified_by = request.user
            form.save()
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

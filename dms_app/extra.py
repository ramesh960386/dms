import csv
from django.http import HttpResponse
from django.template import RequestContext, Template


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


def ip_address_processor(request):
    return {'ip_address': request.META['REMOTE_ADDR']}


def client_ip_view(request):
    template = Template('{{ title }}: {{ ip_address }}')
    context = RequestContext(request, {
        'title': 'Your IP Address',
    }, [ip_address_processor])
    return HttpResponse(template.render(context))

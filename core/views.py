from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from django.core.files.storage import FileSystemStorage
from .models import Document, Person
from .forms import DocumentForm
import datetime

def home(request):
    user = Person.objects.get(username='teacher')
    documents = user.documents.all()
    ip = get_client_ip(request)
    return render(request, 'core/home.html', {'documents': documents,
                                              'ip': ip})

def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'core/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'core/simple_upload.html')


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            ip = get_client_ip(request)
            date = str(datetime.datetime.today().year) + str(datetime.datetime.today().month) + str(datetime.datetime.today().day)
            ip_and_date = ip + "_" + date
            document = Document
            try:
                document = Document.objects.get(ipaddr_and_date=ip_and_date)
            except:
                document = None
            if document != None:
                document.description = form.instance.description
                document.document = form.instance.document
                document.ipaddr_and_date = ip_and_date
                document.updated = datetime.datetime.now()
                document.save()
            else:
                new_form = form.save(commit=False)
                new_form.ipaddr_and_date = ip_and_date
                new_form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'core/model_form_upload.html', {
        'form': form
    })

@ajax_required
@require_POST
def delete_document(request):
    document_id = request.POST.get('id')
    action = request.POST.get('action')
    if document_id and action:
        try:
            if action == 'delete':
                Document.objects.get(id=document_id).delete()
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status':'ko'})

PRIVATE_IPS_PREFIX = ('10.', '172.', '192.', )

def get_client_ip(request):
    """
    Get the client ip from the request
    """
    remote_address = request.META.get('REMOTE_ADDR')
    # set the default value of the ip to be the REMOTE_ADDR if available
    # else None
    ip = remote_address
    # try to get the first non-proxy ip (not a private ip) from the
    # HTTP_X_FORWARDED_FOR
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        proxies = x_forwarded_for.split(',')
        # remove the private ips from the beginning
        while (len(proxies) > 0 and
                proxies[0].startswith(PRIVATE_IPS_PREFIX)):
            proxies.pop(0)
        # take the first ip which is not a private one (of a proxy)
        if len(proxies) > 0:
            ip = proxies[0]
    return ip


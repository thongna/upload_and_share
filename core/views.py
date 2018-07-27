from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from django.core.files.storage import FileSystemStorage
from .models import Document, Person, Department
from .forms import DocumentForm
import datetime
from django.contrib.auth.decorators import login_required

def home(request):
    user = Person.objects.get(username='teacher')
    documents = user.documents.all()
    dpts = Department.objects.filter(available=True)
    ip = get_client_ip(request)

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
                document.department = 'marketing/'
                document.ipaddr_and_date = ip_and_date
                document.updated = datetime.datetime.now()
                document.save()
            else:
                new_form = form.save(commit=False)
                new_form.ipaddr_and_date = ip_and_date
                new_form.department =request.POST.get('department')
                new_form.save()
            return redirect('home')
    else:
        form = DocumentForm()

    return render(request, 'core/home.html', {'documents': documents,
                                              'ip': ip,
                                              'departments': dpts,
                                              'form': form})

@login_required
def share_document(request):
    user = Person.objects.get(username='teacher')
    documents = user.documents.all()
    allOfDocument = Document.objects.all()
    hidden_documents = allOfDocument
    for a in allOfDocument:
        if a in documents:
            hidden_documents = hidden_documents.exclude(id=a.id)
    return render(request, 'core/select-shared-files.html', {'documents': documents,
                                                             'hidden_documents': hidden_documents})

@ajax_required
@require_POST
def save_shared_document(request):
    print('save')
    ids = request.POST.get('id[]')
    user = Person.objects.get(username='teacher')
    documents = user.documents.all()
    document_ids = []
    for document in documents:
        document_ids.append(document.id)
    new_document_ids = []
    if id:
        try:
            for id in ids:
                if id not in document_ids:
                    new_document_ids.append(id)
            cleaned_list = map(int, new_document_ids)
            for new_document_id in cleaned_list:
                user.documents.add(id=new_document_id)
            return JsonResponse({'status': 'ok', 'ids': ids})
        except:
            pass
    return JsonResponse({'status': 'ko', 'ids': ids})

@ajax_required
@require_POST
def delete_document(request):
    document_id = request.POST.get('id')
    action = request.POST.get('action')
    if document_id and action:
        try:
            if action == 'delete':
                Document.objects.get(id=document_id).delete()
            return JsonResponse({'status': 'ok', 'document-id': document_id})
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


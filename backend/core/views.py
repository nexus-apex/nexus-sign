import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count
from .models import Document, SignRequest, Template


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard/')
        error = 'Invalid credentials. Try admin / Admin@2024'
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def dashboard_view(request):
    ctx = {}
    ctx['document_count'] = Document.objects.count()
    ctx['document_draft'] = Document.objects.filter(status='draft').count()
    ctx['document_sent'] = Document.objects.filter(status='sent').count()
    ctx['document_viewed'] = Document.objects.filter(status='viewed').count()
    ctx['signrequest_count'] = SignRequest.objects.count()
    ctx['signrequest_pending'] = SignRequest.objects.filter(status='pending').count()
    ctx['signrequest_signed'] = SignRequest.objects.filter(status='signed').count()
    ctx['signrequest_declined'] = SignRequest.objects.filter(status='declined').count()
    ctx['template_count'] = Template.objects.count()
    ctx['recent'] = Document.objects.all()[:10]
    return render(request, 'dashboard.html', ctx)


@login_required
def document_list(request):
    qs = Document.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(title__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'document_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def document_create(request):
    if request.method == 'POST':
        obj = Document()
        obj.title = request.POST.get('title', '')
        obj.sender = request.POST.get('sender', '')
        obj.status = request.POST.get('status', '')
        obj.signers = request.POST.get('signers') or 0
        obj.sent_date = request.POST.get('sent_date') or None
        obj.completed_date = request.POST.get('completed_date') or None
        obj.file_url = request.POST.get('file_url', '')
        obj.save()
        return redirect('/documents/')
    return render(request, 'document_form.html', {'editing': False})


@login_required
def document_edit(request, pk):
    obj = get_object_or_404(Document, pk=pk)
    if request.method == 'POST':
        obj.title = request.POST.get('title', '')
        obj.sender = request.POST.get('sender', '')
        obj.status = request.POST.get('status', '')
        obj.signers = request.POST.get('signers') or 0
        obj.sent_date = request.POST.get('sent_date') or None
        obj.completed_date = request.POST.get('completed_date') or None
        obj.file_url = request.POST.get('file_url', '')
        obj.save()
        return redirect('/documents/')
    return render(request, 'document_form.html', {'record': obj, 'editing': True})


@login_required
def document_delete(request, pk):
    obj = get_object_or_404(Document, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/documents/')


@login_required
def signrequest_list(request):
    qs = SignRequest.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(document_title__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'signrequest_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def signrequest_create(request):
    if request.method == 'POST':
        obj = SignRequest()
        obj.document_title = request.POST.get('document_title', '')
        obj.signer_name = request.POST.get('signer_name', '')
        obj.signer_email = request.POST.get('signer_email', '')
        obj.status = request.POST.get('status', '')
        obj.sent_date = request.POST.get('sent_date') or None
        obj.signed_date = request.POST.get('signed_date') or None
        obj.ip_address = request.POST.get('ip_address', '')
        obj.save()
        return redirect('/signrequests/')
    return render(request, 'signrequest_form.html', {'editing': False})


@login_required
def signrequest_edit(request, pk):
    obj = get_object_or_404(SignRequest, pk=pk)
    if request.method == 'POST':
        obj.document_title = request.POST.get('document_title', '')
        obj.signer_name = request.POST.get('signer_name', '')
        obj.signer_email = request.POST.get('signer_email', '')
        obj.status = request.POST.get('status', '')
        obj.sent_date = request.POST.get('sent_date') or None
        obj.signed_date = request.POST.get('signed_date') or None
        obj.ip_address = request.POST.get('ip_address', '')
        obj.save()
        return redirect('/signrequests/')
    return render(request, 'signrequest_form.html', {'record': obj, 'editing': True})


@login_required
def signrequest_delete(request, pk):
    obj = get_object_or_404(SignRequest, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/signrequests/')


@login_required
def template_list(request):
    qs = Template.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(name__icontains=search)
    status_filter = ''
    return render(request, 'template_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def template_create(request):
    if request.method == 'POST':
        obj = Template()
        obj.name = request.POST.get('name', '')
        obj.category = request.POST.get('category', '')
        obj.pages = request.POST.get('pages') or 0
        obj.fields_count = request.POST.get('fields_count') or 0
        obj.usage_count = request.POST.get('usage_count') or 0
        obj.active = request.POST.get('active') == 'on'
        obj.description = request.POST.get('description', '')
        obj.save()
        return redirect('/templates/')
    return render(request, 'template_form.html', {'editing': False})


@login_required
def template_edit(request, pk):
    obj = get_object_or_404(Template, pk=pk)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '')
        obj.category = request.POST.get('category', '')
        obj.pages = request.POST.get('pages') or 0
        obj.fields_count = request.POST.get('fields_count') or 0
        obj.usage_count = request.POST.get('usage_count') or 0
        obj.active = request.POST.get('active') == 'on'
        obj.description = request.POST.get('description', '')
        obj.save()
        return redirect('/templates/')
    return render(request, 'template_form.html', {'record': obj, 'editing': True})


@login_required
def template_delete(request, pk):
    obj = get_object_or_404(Template, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/templates/')


@login_required
def settings_view(request):
    return render(request, 'settings.html')


@login_required
def api_stats(request):
    data = {}
    data['document_count'] = Document.objects.count()
    data['signrequest_count'] = SignRequest.objects.count()
    data['template_count'] = Template.objects.count()
    return JsonResponse(data)

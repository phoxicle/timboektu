from models import Post, PostForm, Department
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
import os
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import urllib
from timboektu.books.config import NOTIFY_THRESHOLD, DELETE_THRESHOLD
from django.db.models import Count


import sys

# TODO combine with index, optional department id   
def department(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    return index(request, department)
    
def index(request, department = None):
    query = request.POST.get('query')
    if not query:
        query = request.GET.get('query')
    order_by = request.GET.get('order_by')
    if not order_by:
        order_by = '-crdate'
    page = request.GET.get('page')
        
    # Get posts for query
    #TODO extend .order_by for case insensitivity: .extra(select={'title': 'lower(title)'})
    posts = []
    if query:
        posts = Post.objects.query_filter(query).order_by(order_by)
    else:
        posts = Post.objects.all().order_by(order_by)
        
    # Filter for department 
    if department:
        posts = posts.filter(departments__id=department.id)
        
    # Paging
    num_per_page = 15 if query or department else 5 
    paginator = Paginator(posts, num_per_page)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    
    return render(request, 'index.html', {
        'posts': posts,
        'departments': Department.objects.annotate(my_count=Count('post')),
        'current_department': department,
        'query' : query,
        'title_order_by' : '-title' if order_by == 'title' else 'title',
        'title_order_class' : 'dec' if order_by == 'title' else 'asc' if order_by == '-title' else '',
        'price_order_by' : '-price' if order_by == 'price' else 'price',
        'price_order_class' : 'dec' if order_by == 'price' else 'asc' if order_by == '-price' else '',
    })

def detail(request, post_id):
    p = get_object_or_404(Post, pk=post_id)
    email = urllib.quote(render_to_string('emails/purchase.html', {'post': p}))
    subject = urllib.quote("Interest in your advertisement on TimBoekTU")
    mailto = p.email + '?subject=' + subject + '&body=' + email
    return render(request, 'detail.html', {'post': p, 'mailto': mailto })

def edit(request, post_hash):
    p = get_object_or_404(Post, hash=post_hash)
    # Update
    if request.method == 'POST':
        form = PostForm(request.POST, instance=p)
        if form.is_valid():
            p.set_isbn_int()
            p.save()
            return HttpResponseRedirect(reverse('timboektu.books.views.detail', kwargs={'post_id': p.id}))
    # Edit
    else:
        form = PostForm(instance=p) 
    return render(request, 'edit.html', {
        'form' : form,
        'post' : p,
        'delete' : DELETE_THRESHOLD
    })
    
def new(request):
    # Create
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            p = form.save()
            p.hash = (os.urandom(16)).encode('hex')
            p.set_isbn_int()
            
            # Send edit link to user
            send_mail(
                      'TimBoekTU edit link for ' + p.title,
                       render_to_string('emails/edit.html', {'post' : p}), 
                       'services@timboektu.com',
                       [p.email], 
                       fail_silently=True)
            
            p.save()
            return HttpResponseRedirect(reverse('timboektu.books.views.confirm', kwargs={'post_hash': p.hash}))
    # New
    else:
        form = PostForm()
    return render(request, 'edit.html', {
        'form' : form,
        'delete' : DELETE_THRESHOLD
    })
    
def confirm(request, post_hash):
    p = get_object_or_404(Post, hash=post_hash)
    return render(request, 'confirm.html', {
        'post' : p,
    })
    
def renew(request, post_hash):
    p = get_object_or_404(Post, hash=post_hash)
    p.save() # Updates mdate, notified
    return render(request, 'renew.html', {
        'post' : p,
    })

def delete(request):
    post_hash = request.GET.get('hash')
    p = get_object_or_404(Post, hash=post_hash)
    p.delete()
    return render(request, 'delete.html')
    
def about(request):
    return render(request, 'about.html')
    
def contribute(request):
    return render(request, 'contribute.html')

def locations(request):
    return render(request, 'locations.html')

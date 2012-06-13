from models import Post, PostForm, Department, PostManager
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
import time
import os
from django.core.mail import send_mail

import sys

# TODO combine with index, optional department id   
def department(request, department_id, order_by = '-crdate'):
    department = get_object_or_404(Department, pk=department_id)
    return index(request, department, order_by)
    
def index(request, department = None, order_by = '-crdate'):
    # Check for submitted query
    query = request.POST.get('query')
        
    # Get posts for query
    #TODO extend .order_by for case insensitivity: .extra(select={'lower_name': 'lower(name)'})
    posts = []
    if query:
        posts = PostManager().query(query).order_by(order_by)
    else:
        posts = Post.objects.all().order_by(order_by)
        
    # Filter for department 
    if department:
        posts = posts.filter(departments__id=department.id)
        
    return render(request, 'index.html', {
        'latest_posts': posts[:5],
        'departments': Department.objects.all(),
        'current_department': department,
        'query' : query,
        'title_order_by' : '-title' if order_by == 'title' else 'title',
        'title_order_class' : 'dec' if order_by == 'title' else 'asc' if order_by == '-title' else '',
        'price_order_by' : '-price' if order_by == 'price' else 'price',
        'price_order_class' : 'dec' if order_by == 'price' else 'asc' if order_by == '-price' else '',
    })

def detail(request, post_id):
    import urllib
    p = get_object_or_404(Post, pk=post_id)
    email = urllib.quote_plus(render_to_string('email.html', {'post': p}))
    subject = urllib.quote_plus("Your advertisement on TimBoekTU")
    mailto = p.email + '?subject=' + subject + '&body=' + email
    return render(request, 'detail.html', {'post': p, 'mailto': mailto })

def edit(request, post_hash):
    p = get_object_or_404(Post, hash=post_hash)
    # Update
    if request.method == 'POST':
        form = PostForm(request.POST, instance=p)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('timboektu.books.views.index'))
    # Edit
    else:
        form = PostForm(instance=p) 
    return render(request, 'edit.html', {
        'form': form,
        'post' : p
    })
    
def new(request):
    # Create
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            p = form.save()
            p.hash = (os.urandom(16)).encode('hex')
            # Send edit link to user
            send_mail(
                      'TimBoekTU edit link for ' + p.title,
                       render_to_string('email_edit.html', {'post' : p}), 
                       'from@example.com',
                       ['cgerpheide@gmail.com'], fail_silently=True)
            p.save()
            return HttpResponseRedirect(reverse('timboektu.books.views.confirm', kwargs={'post_hash': p.hash}))
    # New
    else:
        form = PostForm()
    return render(request, 'edit.html', {
        'form': form,
    })
    
def confirm(request, post_hash):
    p = get_object_or_404(Post, hash=post_hash)
    return render(request, 'confirm.html', {
        'post': p,
    })
    
def about(request):
    return render(request, 'about.html')
    
def contact(request):
    return render(request, 'contact.html')

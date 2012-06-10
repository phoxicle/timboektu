from django.template import RequestContext, Context, loader
from models import Post
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404

import sys

def index(request):
    latest_posts = Post.objects.all().order_by('-crdate')[:5]
    t = loader.get_template('index.html')
    c = Context({
        'latest_posts': latest_posts,
    })
    return HttpResponse(t.render(c))

def detail(request, post_id):
    p = get_object_or_404(Post, pk=post_id)
    return render_to_response('detail.html', {'post': p})

def edit(request, post_id):
    p = get_object_or_404(Post, pk=post_id)
    return render_to_response('edit.html', {'post': p}, context_instance=RequestContext(request))

def update(request, post_id):
    p = get_object_or_404(Post, pk=post_id)
    p.title = request.POST.get('title')
    p.save()
    return HttpResponseRedirect(reverse('timboektu.books.views.detail', args=(p.id,)))
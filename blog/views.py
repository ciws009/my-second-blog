from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post
from django.contrib import messages
from django.db.models import Q
from functools import reduce
from operator import and_
from .lib import get_cosine_similarity_with_pk_from_posts

def post_list(request):
     posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
     keyword = request.GET.get('keyword')
     
     if keyword:
          q_list = ''
          exclusion = set([' ', '　'])
          for k in keyword:
               if k in exclusion:
                    pass
               else:
                   q_list+=k
          x = reduce(and_, [Q(title__icontains=q) for q in q_list])
          y = reduce(and_, [Q(text__icontains=q) for q in q_list])
          posts = Post.objects.filter(x | y)
          messages.success(request, f'「{keyword}」の検索結果')     
     return render(request, 'blog/post_list.html', {'posts':posts})

def post_detail(request, pk):
     post = get_object_or_404(Post, pk=pk)     
     posts = Post.objects.filter(published_date__isnull=False) 
     cosine_similarity = get_cosine_similarity_with_pk_from_posts(posts)
     related_posts_pks = cosine_similarity[post.pk]
     related_posts_titles = {}
     for related_pk in related_posts_pks:
          p = Post.objects.filter(pk=related_pk[0])
          related_posts_titles[related_pk[0]] = p[0]
     return render(request, 'blog/post_detail.html', {'post':post, 'related_posts_titles':related_posts_titles})

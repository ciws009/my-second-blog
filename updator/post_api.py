from blog.models import Post
from blog.lib import get_cosine_similarity_with_pk_from_posts

def update_related_post_titles():
    posts = Post.objects.filter(published_date__isnull=False)

    for post in posts:
        cosine_similarity = get_cosine_similarity_with_pk_from_posts(posts)
        related_posts_pks = cosine_similarity[post.pk]
        for related_pk in related_posts_pks:
            p = Post.objects.filter(pk=related_pk[0])
            post.related_post_titles[related_pk[0]] = p[0]
        post.save(update_fields=['related_post_titles'])

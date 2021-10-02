from typing import List
from django.contrib import admin
from .models import Post
from django_summernote.admin import SummernoteModelAdmin

class blogadmin(SummernoteModelAdmin):
    summernote_fields = '__all__'

admin.site.register(Post, blogadmin)


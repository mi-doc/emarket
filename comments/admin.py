from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

# Register your models here.
from .models import Comment


class CommentsInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ('responded_user',)

    def get_fields(self, request, obj=None):
        return [
            'responded_user',
            'content'
        ]

    def responded_user(self, obj):
        comment_id = obj.id
        url = reverse('admin:comments_comment_change', args=(obj.id,))
        return format_html(f'<a href="{url}">{obj.user}</a>')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    fields = [
        'user',
        'content_type',
        'product',
        'object_id',
        'content',
        'parent_comment_author',
        'parent_comment_text'
    ]

    list_display = [
        'user',
        'content_type',
        'product',
        'parent_comment_author',
        'text',
        'timestamp'
    ]

    readonly_fields = ('parent_comment_author', 'product', 'parent_comment_text')


    def product(self, obj):
        url = reverse('admin:products_product_change', args=(obj.content_object.id,))
        return format_html(f'<a href="{url}">{obj.content_object}</a>')

    def parent_comment_author(self, obj):
        parent_comment_id = getattr(obj.parent, 'id', None)
        if not parent_comment_id:
            return '-'
        url = reverse('admin:comments_comment_change', args=(obj.parent.id,))
        return format_html(f'<a href="{url}">{obj.parent.user}</a>')

    def parent_comment_text(self, obj):
        parent_comment_id = getattr(obj.parent, 'id', None)
        if not parent_comment_id:
            return '-'
        return obj.parent.content


    def text(self, obj):
        text = obj.content
        content = (text[:50] + '...') if len(text) > 50 else text
        url = reverse('admin:comments_comment_change', args=(obj.id,))
        return format_html(f'<a href="{url}">{content}</a>')

    inlines = [CommentsInline]
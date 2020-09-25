import django_filters
from .models import Post


class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['user','created_by','content', 'img', 'created_at', 'active']

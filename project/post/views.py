from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .models import Post
from .forms import PostForm
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .filters import PostFilter
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView


# Start Of Class Based view
class PostList(ListView):
    model = Post  # in template context is : [object_list or post_list]
    context_object_name = 'all_post'
    queryset = Post.objects.filter(active=True)
    template_name = 'post_list.html'
    paginate_by = 3

    def paginate_queryset(self, queryset, page_size):
        try:
            return super(PostList, self).paginate_queryset(queryset, page_size)
        except Http404:
            self.kwargs['page'] = 1
            return super(PostList, self).paginate_queryset(queryset, page_size)

    def get_queryset(self):
        queryset = Post.objects.filter(active=True)
        my_filter = PostFilter(self.request.GET, queryset)
        queryset = my_filter.qs
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['myname'] = 'MuuHamed14'
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'id'


class PostCreate(CreateView):
    model = Post
    template_name = 'post_create.html'
    fields = ['title', 'content', 'img']

    def form_valid(self, form):
        new_form = form.save(commit=False)
        new_form.user = self.request.user
        form.save()
        return redirect('blog:all_posts1')


class PostUpdate(UpdateView):
    model = Post
    template_name = 'post_update.html'
    fields = ['title', 'content', 'img']
    pk_url_kwarg = 'id'

    def form_valid(self, form):
        new_form = form.save(commit=False)
        new_form.user = self.request.user
        form.save()
        return redirect('blog:all_posts1')


# End Of Class Based view

# Start Of functional Based View
def all_posts(request):
    all_post = Post.objects.filter(active=True)
    my_filter = PostFilter(request.GET, queryset=all_post)
    all_post = my_filter.qs
    paginator = Paginator(all_post, 3)
    page = request.GET.get('page')
    try:
        all_post = paginator.page(page)
    except PageNotAnInteger:
        all_post = paginator.page(1)
    except EmptyPage:
        all_post = paginator.page(paginator.num_pages)
    return render(request, 'all_posts.html', {'all_post': all_post, 'my_filter': my_filter})


def one_post(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'detail.html', {'post': post})


def create_post(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form1 = form.save(commit=False)
            form1.user = request.user
            form1.created_by = request.user
            form1.save()
            messages.success(request, 'Post Created Successfully')
            return redirect('blog:all_posts')
        else:
            form = PostForm()
    return render(request, 'create_post.html', {'form': form})


def edit_post(request, id):
    post = get_object_or_404(Post, id=id)
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form1 = form.save(commit=False)
            form1.user = request.user
            form1.save()
            messages.success(request, 'Post Edited Successfully')
            return redirect('blog:all_posts')
        else:
            form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form})
# End Of functional Based View

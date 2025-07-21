from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.decorators.cache import never_cache
from django.views.generic.detail import DetailView


# Create your views here.
@never_cache
@login_required
def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {"posts" :posts})

#View Details
@login_required
def post_details(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post':post})

#New Post
class PostCreateView(CreateView):
    model = Post
    template_name = "blog/post_form.html"
    fields = ["title", "content", "image"]
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.author = self.request.user  # ← inilah kuncinya!
        return super().form_valid(form)


#Update Post
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = "blog/post_form.html"
    fields = ["title", "content", "image"]
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        # Debug info
        print("FILES:", self.request.FILES)
        print("POST:", self.request.POST)
        
        # Ambil instance yang akan diupdate
        self.object = form.save(commit=False)
        
        if 'image' in self.request.FILES:
            # Jika ada gambar baru
            if self.object.image:
                # Simpan referensi gambar lama
                old_image = Post.objects.get(pk=self.object.pk).image
                try:
                    # Hapus gambar lama
                    old_image.delete(save=False)
                except Exception as e:
                    print(f"Error deleting old image: {e}")
            
            # Set gambar baru
            self.object.image = self.request.FILES['image']
        else:
            # Jika tidak ada gambar baru, pertahankan gambar lama
            if self.object.pk:
                original = Post.objects.get(pk=self.object.pk)
                self.object.image = original.image
        
        # Simpan perubahan
        self.object.save()
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_staff
#

#Delete Post
class PostDeleteView(DeleteView, LoginRequiredMixin, UserPassesTestMixin):
    model = Post
    template_name = "blog/post_delete.html"
    success_url = reverse_lazy("home")

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_staff
    

#Post Detail View
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
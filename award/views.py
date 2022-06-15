from django.shortcuts import render, get_object_or_404, redirect 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from django.contrib.auth.views import LoginView
from .models import Post, Profile
from .forms import PostForm, EditForm
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm
from django.urls import reverse_lazy,reverse
from django.contrib.auth.views import PasswordResetView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.
def index(request):
    return render(request, 'users/index.html')

def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='/')

        return render(request, self.template_name, {'form': form})

class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('index')


@login_required
def profile(request):
    # project_form = ProjectForm()
    current_user = request.user
    profile = Profile.objects.filter(user = current_user.pk).first()
    # projects = Project.objects.filter(profile = profile).all()

    return render (request, 'users/profile.html', {"profile":profile, "current_user":current_user})

def update_profile(request):
    current_user = request.user
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            profile = form.save(commit = False)
            profile.save()

        return redirect("profile", id = current_user.id )   

    else:
        form = UpdateProfileForm()  

    return render(request, 'users/update_profile.html', {"current_user":current_user , "form":form})

    # if request.method == 'POST':
    #     # profile = UserProfile.objects.create(user=request.user)
    #     user_form = UpdateUserForm(request.POST, instance=request.user)
    #     profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.Profile.user)

    #     if user_form.is_valid() and profile_form.is_valid():
    #         user_form.save()
    #         profile_form.save()
    #         messages.success(request, 'Your profile is updated successfully')
    #         return redirect(to='users-profile')
    # else:
    #     user_form = UpdateUserForm(instance=request.user)
    #     profile_form = UpdateProfileForm(instance=request.Profile.user)

    # return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('index')


class ArticleDetailView(DetailView):
    model = Post
    template_name = 'article_details.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()

        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True

        context["total_likes"] = total_likes
        context["liked"] = liked
        return context


class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'users/add_post.html'
    # fields = '__all__'
    # fields = ('title', 'body')

# class AddCategoryView(CreateView):
#     model = Category
#     # form_class = PostForm
#     template_name = 'add_category.html'
#     fields = '__all__'
#     # fields = ('title', 'body')

class UpdatePostView(UpdateView):
    model = Post
    form_class = EditForm
    template_name = 'update_post.html'
    # fields = ['title', 'title_tag', 'body']

class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')

def Search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        posts = Post.objects.filter(title__icontains=searched)
        return render(request, 'users/search.html', {'searched':searched, 'posts': posts})

    else:
        return render(request, 'users/search.html', {}) 

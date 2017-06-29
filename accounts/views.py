from .models import UserProfile
from comments.forms import CommentForm
from comments.models import Comment
#  from django.conf import settings
from django.db.models import Q
from django.contrib import messages

#  from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect  # Http404   HttpResponse

from django.views.generic import RedirectView
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)

from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,

)
from .forms import UserLoginForm, UserRegisterForm, UserProfileForm


# Create your views here.
def profile_edit(request, slug=None):
    instance = get_object_or_404(UserProfile, slug=slug)
    form = UserProfileForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        # message success
        messages.success(request, "item saved")
        return HttpResponseRedirect(instance.get_absolute_url())

    return render(request, "form.html", context={"form": form, "title": "edit"})


def profile_detail(request, slug=None):
    profile_instance = get_object_or_404(UserProfile, slug=slug)
    user_ = None
    if request.user.is_authenticated:
        user_ = get_object_or_404(UserProfile, user=request.user)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        content = form.cleaned_data.get("content")
        parent = None
        new_comment = Comment.objects.create(
            user=request.user,
            content=content,
            parent=parent,
        )
        try:
            parent = int(request.POST.get("parent_id"))
        except:
            parent = None
        if (parent):
            new_comment.parent = Comment.objects.filter(id=parent).first()
            new_comment.save()

        return HttpResponseRedirect(profile_instance.get_absolute_url())

    qs_comments = Comment.objects.filter(user=profile_instance.user, parent=None)
    content = {
        "profile": profile_instance,
        'form': form,
        "comments": qs_comments,
        "user_": user_,
    }
    return render(request, "detail.html", content)


def profile_list(request):
    pass
    # qs = UserProfile.objects.all()
    # content = {
    #     "profiles": qs,
    # }
    # return render(request, "list.html", content)


def about(request):
    return render(request, "about.html")


def search(request):
    if (request.user.is_authenticated()):
        query = request.GET.get("search")
        user_ = get_object_or_404(UserProfile, user=request.user)
        print query
        query_list = None
        if query:
            query_list = UserProfile.objects.filter(
                Q(user__username__icontains=query) |
                Q(interests__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
            ).distinct()
        print query_list
        context = {
            'users': query_list,
            'user_': user_,
            'all_users': UserProfile.objects.all(),
        }

        return render(request, "search_profiles.html", context)
    else:
        return redirect("login")


def main_page(request):
    form = CommentForm(request.POST or None)
    query_list_users = None
    query_list_users_all = UserProfile.objects.all()
    user = request.user
    comments = None
    user_ = None
    if user.is_authenticated():
        user_ = get_object_or_404(UserProfile, user=request.user)
        query_list_users = UserProfile.objects.filter(interests__icontains=user_.interests).exclude(user=request.user)
        comments = Comment.objects.filter(user__in=(user_.followers.all()))
    print query_list_users
    content = {
        "comments": comments,
        "user_": user_,
        'form': form,
        "users": query_list_users,
        "all_users": query_list_users_all,
    }
    return render(request, "list.html", content)
    # return redirect("accounts:list")


class CommentLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        comment_id = self.kwargs.get("comment_id")
        print (comment_id)
        comment_instance = get_object_or_404(Comment, id=comment_id)
        profile_instance = get_object_or_404(UserProfile, user=comment_instance.user)
        url_ = profile_instance.get_absolute_url()
        user = self.request.user
        if user.is_authenticated():
            if user in comment_instance.likes.all():
                comment_instance.likes.remove(user)
            else:
                comment_instance.likes.add(user)
        else:
            return "/login"
        return url_


class FollowToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            slug = self.kwargs.get("slug")
            print (slug)
            profile_instance = get_object_or_404(UserProfile, slug=slug)
            url_ = profile_instance.get_absolute_url()
            user_ = get_object_or_404(UserProfile, user=self.request.user)
            if profile_instance.user in user_.followers.all():
                user_.followers.remove(profile_instance.user)
            else:
                user_.followers.add(profile_instance.user)
            print (user_.user)
            print (user_.followers.all())
            return url_
        else:
            return "/login"


# Login & Logout & Registration Functions from Course try-django 1.9 not from me

def login_view(request):
    if (not request.user.is_authenticated()):
        # next = request.GET.get('next')
        title = "Login"
        form = UserLoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            # if next:
            #     return redirect(next)
            return redirect("/")
        return render(request, "form.html", {"form": form, "title": title})
    else:
        redirect("/")


def register_view(request):
    if (not request.user.is_authenticated):
        # next = request.GET.get('next')
        title = "Register"
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            new_user = authenticate(username=user.username, password=password)
            login(request, new_user)
            # if next:
            #     return redirect(next)
            return redirect("/")
    else:
        return redirect("/")
    context = {
        "form": form,
        "title": title
    }
    return render(request, "form.html", context)


def logout_view(request):
    logout(request)
    return redirect("/")

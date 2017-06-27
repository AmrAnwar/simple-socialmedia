from .models import UserProfile
from comments.forms import CommentForm
from comments.models import Comment
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404  # HttpResponse

from django.views.generic import RedirectView
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)


# Create your views here.
def profile_detail(request, slug=None):
    profile_instance = get_object_or_404(UserProfile, slug=slug)
    form = CommentForm(request.POST or None)

    if form.is_valid():
        content = form.cleaned_data.get("content")
        parent = None
        new_comment = Comment.objects.create(
            user=request.user,
            content=content,
            parent=parent
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
    }

    return render(request, "detail.html", content)


def profile_list(request):
    qs = UserProfile.objects.all()
    content = {
        "profiles": qs,
    }
    return render(request, "list.html", content)


def main_page(request):
    return redirect("accounts:list")


class CommentLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        # slug = self.kwargs.get("slug")
        # print (slug)
        comment_id = self.kwargs.get("comment_id")
        print (comment_id)
        comment_instance = get_object_or_404(Comment, id=comment_id)
        profile_instance = get_object_or_404(UserProfile, user=comment_instance.user)
        url = profile_instance.get_absolute_url()
        user = self.request.user
        if user.is_authenticated():
            if user in comment_instance.likes.all():
                comment_instance.likes.remove(user)
            else:
                comment_instance.likes.add(user)
        return (url)

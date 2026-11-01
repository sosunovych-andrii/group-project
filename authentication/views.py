from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm


@login_required(login_url="login")
def profile(request):
    return render(request, "profile.html", {"user": request.user})


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form},
    )

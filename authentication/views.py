from django.shortcuts import render,redirect
from .forms import RegisterForm
from django.conf import settings
from django.contrib.auth.decorators import login_required



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
        "account/register.html",
        {"form":form}
    )
@login_required
def my_view(request):
    if not request.user.is_authenticated:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")




# Create your views here.

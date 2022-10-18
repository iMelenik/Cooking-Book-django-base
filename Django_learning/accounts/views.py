from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


# Create your views here.
def login_view(request):
    contex = {}

    if request.POST:
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        # user = authenticate(request, username=username, password=password)
        # if user:
            login(request, form.get_user())
            return redirect('/')
        else:
            contex['error'] = 'Неверное имя и/или пароль.'
    else:
        form = AuthenticationForm(request)
    contex['form'] = form
    return render(request, 'accounts/login.html', context=contex)


def register_view(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        return redirect('/login/')
    contex = {'form': form}
    return render(request, 'accounts/register.html', context=contex)


def logout_view(request):
    contex = {}
    if request.POST:
        logout(request)
    return render(request, 'accounts/logout.html', context=contex)

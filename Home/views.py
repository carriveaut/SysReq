from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

# class SignUpView(generic.CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy('index')
#     template_name = 'Registration/signup.html'
success = False
badData = "False"


def set_success(suc):
    global success
    success = suc


def get_success():
    return success


def register(request):
    noGood = "False"
    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            set_success(True)
            success = get_success()
            print(success)
            return render(request, 'Home/index.html', {'success': success})
        else:
            noGood = "True"
            messages.error(request, "Error")
            set_success(False)
            success = get_success()
            print(success)
    else:
        f = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': f, 'badData': noGood})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('Home:account')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'Home/account.html', {
        'form': form,
    })


def index(request):
    return render(request, 'Home/index.html')


def helps(request):
    return render(request, 'Home/help.html')


def happeningsoon(request):
    return render(request, 'Home/happeningsoon.html')


def deals(request):
    return render(request, 'Home/deals.html')



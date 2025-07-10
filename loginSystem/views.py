from django.shortcuts import render, redirect
from .models import EmployeeUser
from .forms import EmployeeLoginForm
from django.contrib.auth.hashers import check_password
from django.contrib import messages

def employee_login(request):
    form = EmployeeLoginForm()

    if request.method == 'POST':
        form = EmployeeLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = EmployeeUser.objects.get(username=username)
                if check_password(password, user.password):
                    request.session['employee_user_id'] = user.id
                    return redirect('homeSystem:home')  # or your dashboard
                else:
                    messages.error(request, "Incorrect password.")
            except EmployeeUser.DoesNotExist:
                messages.error(request, "User not found.")

    return render(request, 'loginSystem/login.html', {'form': form})

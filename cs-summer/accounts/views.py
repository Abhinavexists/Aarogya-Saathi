from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from .forms import SignupForm, LoginForm
from .models import UserProfile
from django.contrib import messages


def home_view(request):
    # This is the view for the homepage with login and signup links
    return render(request, 'home.html')
# accounts/views.py



def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()  # Save the user profile to the database
            messages.success(request, "Signup successful! Please log in.")
            return redirect('login')  # Redirect to login page after signup
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = UserProfile.objects.get(email=email)
            if check_password(password, user.password):
                request.session['user_name'] = user.full_name  # Store user name in session
                messages.success(request, "Successfully logged in!")
                return redirect('chat')
            else:
                messages.error(request, "Invalid password. Please try again.")
        
        except UserProfile.DoesNotExist:
            messages.error(request, "No account found with this email address.")
    
    return render(request, 'login.html')

def chat_view(request):
    user_name = request.session.get('user_name', 'User')  # Retrieve user name from session
    return render(request, 'chat.html', {'user_name': user_name})
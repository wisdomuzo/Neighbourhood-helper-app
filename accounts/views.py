from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm
from .forms import UserProfileForm
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.middleware.csrf import get_token
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import get_user_model
from .models import UserRating

@csrf_protect
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('registration_success')

              # Redirect to dashboard after registration
        else:
            messages.error(request, 'Please correct the errors .')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def registration_success(request):
    return render(request, 'registration_success.html')


def login_view(request):
    # Clear all messages before rendering the login page
    storage = messages.get_messages(request)
    list(storage)
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('dashboard')  # Redirect to dashboard after login
            else:
                messages.error(request, 'Invalid email or password.')
        else:
            messages.error(request, 'Invalid email or password.')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


    
@login_required(login_url='login')
def dashboard_view(request):
    return render(request, 'dashboard.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')

# Password request view

User = get_user_model()  # Use this to get your custom user model
def password_reset_request_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            # Generate token and uid for the user
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Redirect user to reset confirmation form with generated token and uid
            reset_url = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            return redirect(reset_url)
        else:
            messages.error(request, 'No account found with this email address.')

    return render(request, 'password_reset_request.html')  # Form where the user enters their email
# Views for handling profile creation and editing 
@login_required
def create_or_edit_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view')  # Redirect to a profile view page
        else:
            print(form.errors)  # Debugging: Print errors if form fails

    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'create_or_edit_profile.html', {'form': form})

@login_required
def view_profile(request):
    user_profile = request.user.userprofile
    return render(request, 'view_profile.html', {'profile': user_profile})


# Users' rating view
@login_required
def rate_user(request, user_id):
    rated_user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        review = request.POST.get('review')
        UserRating.objects.create(rated_user=rated_user, rated_by=request.user, rating=rating, review=review)
        return redirect('dashboard')  # Redirect after successful submission
    return render(request, 'rate_user.html', {'rated_user': rated_user})
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Book, UserProfile, Order

def home(request):
    trending_books = Book.objects.all().order_by('-rating')[:5]
    return render(request, 'index.html', {'trending_books': trending_books})

def user_login(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        try:
            profile = UserProfile.objects.get(phone_number=phone_number)
            user = profile.user
            user = authenticate(request, username=user.username, password=password)
            if user is not None and not profile.is_author:
                login(request, user)
                return redirect('user_account')  # Redirect to user account
            else:
                messages.error(request, 'Invalid phone number or password, or you are not a user.')
        except UserProfile.DoesNotExist:
            messages.error(request, 'Phone number does not exist.')
    return render(request, 'login.html', {'login_type': 'user'})

def author_login(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        try:
            profile = UserProfile.objects.get(phone_number=phone_number)
            user = profile.user
            user = authenticate(request, username=user.username, password=password)
            if user is not None and profile.is_author:
                login(request, user)
                return redirect('author_account')  # Redirect to author account
            else:
                messages.error(request, 'Invalid phone number or password, or you are not an author.')
        except UserProfile.DoesNotExist:
            messages.error(request, 'Phone number does not exist.')
    return render(request, 'login.html', {'login_type': 'author'})

def user_logout(request):
    logout(request)
    return redirect('home')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        is_author = request.POST.get('is_author') == 'on'

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('register')

        if UserProfile.objects.filter(phone_number=phone_number).exists():
            messages.error(request, 'Phone number already exists.')
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        UserProfile.objects.create(user=user, phone_number=phone_number, is_author=is_author)
        messages.success(request, 'Registration successful. Please log in.')
        return redirect('login')

    return render(request, 'register.html')

def user_account(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.profile.is_author:
        return redirect('author_account')
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'user_account.html', {'orders': orders})

def author_account(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.profile.is_author:
        return redirect('user_account')
    books = Book.objects.filter(author=request.user).order_by('title')
    return render(request, 'author_account.html', {'books': books})

def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    return render(request, 'book_detail.html', {'book': book})
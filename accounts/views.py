from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

from .forms import (
    UserRegistrationForm,
    UserLoginForm,
    UserProfileForm,
    PasswordChangeCustomForm,
)
from orders.models import Order
from wishlist.models import Wishlist
from reviews.models import Review


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to BookNest, {user.get_short_name()}!')
            return redirect('/')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            if user and user.is_active:
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_short_name()}!')
                next_url = request.GET.get('next', '/')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'You have been logged out successfully.')
    return redirect('/')


@login_required
def profile_view(request):
    user_orders = Order.objects.filter(user=request.user)[:5]
    user_wishlist = Wishlist.objects.filter(user=request.user)[:5]
    user_reviews = Review.objects.filter(user=request.user)[:5]

    total_orders_count = Order.objects.filter(user=request.user).count()
    wishlist_count = Wishlist.objects.filter(user=request.user).count()
    reviews_count = Review.objects.filter(user=request.user).count()
    total_spent = Order.objects.filter(user=request.user).aggregate(
        total=Sum('total')
    )['total'] or 0

    context = {
        'user_orders': user_orders,
        'user_wishlist': user_wishlist,
        'user_reviews': user_reviews,
        'total_orders_count': total_orders_count,
        'wishlist_count': wishlist_count,
        'reviews_count': reviews_count,
        'total_spent': total_spent,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = UserProfileForm(
            request.POST, request.FILES, instance=request.user
        )
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'accounts/profile_edit.html', {'form': form})


@login_required
def password_change_view(request):
    if request.method == 'POST':
        form = PasswordChangeCustomForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been changed successfully.')
            return redirect('accounts:profile')
    else:
        form = PasswordChangeCustomForm(request.user)
    return render(request, 'accounts/password_change.html', {'form': form})

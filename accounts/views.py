from django.conf import settings
from django.shortcuts import redirect, render
from accounts.forms import SignupForm
from .models import Profile
from django.contrib.auth.decorators import login_required


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            return redirect(settings.LOGIN_URL)
    else:
        form = SignupForm()
    return render(request, 'accounts/signup_form.html', {
        'form': form,
    })

@login_required
def profile(request):
    # profile = Profile.objects.get(id=user_id)
    # shortname restaurant_name comment.pk
    return render(request, 'accounts/profile.html')


from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib import messages
from .forms import RegisterForm
from .forms import CustomAuthenticationForm
from .models import Activity
from django.core.exceptions import ValidationError
from .forms import ActivityForm
from django.contrib.auth.decorators import login_required

def base(request):
    activities = Activity.objects.all()
    return render(request, "registration/accueil.html", {'activities': activities})

def activity_detail(request, pk):
    activity = Activity.objects.get(pk=pk)
    return render(request, "registration/activity_detail.html", {
        'activity': activity,
    })

def unsubscribe_activity(request, pk):
    activity = Activity.objects.get(pk=pk)
    if request.user in activity.attendees.all():
        activity.attendees.remove(request.user)
        messages.success(request, "Vous vous êtes désinscrit de l'activité.")
    else:
        messages.warning(request, "Vous n'êtes pas inscrit à cette activité.")
    return redirect('activity_detail', pk=pk)

def subscribe_activity(request, pk):
    activity = Activity.objects.get(pk=pk)
    if request.user not in activity.attendees.all():
        activity.attendees.add(request.user)
        messages.success(request, "Vous vous êtes inscrit à l'activité.")
    else:
        messages.warning(request, "Vous êtes déjà inscrit à cette activité.")
    return redirect('activity_detail', pk=pk)

def custom_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bienvenue {user.username} !")
                return redirect('home')
    else:
        form = CustomAuthenticationForm()

    return render(request, "registration/login.html", {'form': form})

def custom_logout(request):
    logout(request)
    messages.success(request, 'Vous êtes déconnecté avec succès.')
    return redirect('login')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Compte créé avec succès !')
            return redirect('login')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = RegisterForm()

    return render(request, 'registration/signup.html', {'form': form})

def create_activity(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            try:
                activity = form.save(commit=False)
                activity.proposer = request.user
                activity.save()

                messages.success(
                    request,
                    f'Votre activité "{activity.title}" a été créée avec succès !'
                )
                return redirect('home')

            except ValidationError as e:
                for field, errors in e.message_dict.items():
                    for error in errors:
                        form.add_error(field, error)
                messages.error(
                    request,
                    'Veuillez corriger les erreurs ci-dessous.'
                )
        else:
            messages.error(
                request,
                'Veuillez corriger les erreurs ci-dessous.'
            )
    else:
        form = ActivityForm()

    return render(request, 'registration/create_activity.html', {
        'form': form,
    })


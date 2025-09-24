from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages
from .forms import CustomAuthenticationForm, EditProfileForm, ActivityForm, RegisterForm
from .models import Activity, User, Category
from django.core.exceptions import ValidationError
from django.conf import settings
from django.core.paginator import Paginator


def base(request):
    activities = Activity.objects.all()
    categories = Category.objects.all()
    category_id = request.GET.get('category')
    show_mes_activities = request.GET.get('mes_activities')
    show_mes_inscriptions = request.GET.get('mes_inscriptions')

    if category_id:
        activities = activities.filter(category__id=category_id)
    if show_mes_activities == 'true' and request.user.is_authenticated:
        activities = activities.filter(proposer=request.user)
    if show_mes_inscriptions == 'true' and request.user.is_authenticated:
        activities = activities.filter(attendees=request.user)

    paginator = Paginator(activities, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'activities': activities,
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': category_id,
        'show_mes_activities': show_mes_activities,
        'show_mes_inscriptions': show_mes_inscriptions,
        'MEDIA_URL': settings.MEDIA_URL,
    }

    return render(request, "registration/accueil.html", context)

def page404(request):
    return render(request, "404.html", status=404)

def page500(request):
    return render(request, "500.html", status=500)

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
    return redirect('home')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
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

def profile(request, id=None):
    MEDIA_URL = settings.MEDIA_URL
    user = get_object_or_404(User, id=id)
    return render(request, 'registration/profile.html', {'MEDIA_URL': MEDIA_URL , 'user': user})

def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil mis à jour avec succès !')
            return redirect('profile', id=request.user.id)
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')

    form = EditProfileForm(instance=request.user)
    return render(request, 'registration/edit_profile.html', {'form': form})

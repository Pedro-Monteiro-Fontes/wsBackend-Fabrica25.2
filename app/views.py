from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Team, PlayerProfile, User
from .forms import PlayerProfileForm, PlayerUserCreationForm
from django.contrib.auth import login

def home(request):
    team = Team.objects.first()
    return render(request, 'app/home.html', {'team': team})

@login_required
def dashboard(request):
    if request.user.is_coach():
        return redirect('coach_dashboard')
    else:
        return redirect('player_dashboard')

@user_passes_test(lambda u: u.is_coach())
def coach_dashboard(request):
    teams = request.user.teams.all()
    players = PlayerProfile.objects.filter(team__in=teams)
    return render(request, 'app/coach_dashboard.html', {'players': players, 'teams': teams})

@login_required
def player_dashboard(request):
    profile = get_object_or_404(PlayerProfile, user=request.user)
    team_players = PlayerProfile.objects.filter(team=profile.team)
    return render(request, 'app/player_dashboard.html', {'players': team_players})

@user_passes_test(lambda u: u.is_coach())
def add_player(request, team_id):
    team = get_object_or_404(Team, id=team_id, coach=request.user)
    if request.method == 'POST':
        user_form = PlayerUserCreationForm(request.POST)
        profile_form = PlayerProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.role = 'player'
            user.set_password(user_form.cleaned_data['password1'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.team = team
            profile.save()
            return redirect('coach_dashboard')
    else:
        user_form = PlayerUserCreationForm(initial={'role': 'player'})
        profile_form = PlayerProfileForm()
    return render(request, 'app/add_player.html', {'user_form': user_form, 'profile_form': profile_form, 'team': team})

@user_passes_test(lambda u: u.is_coach())
def edit_player_stats(request, player_id):
    profile = get_object_or_404(PlayerProfile, id=player_id)
    # Permite edição apenas se o jogador pertence a um time do coach
    if profile.team.coach != request.user:
        return redirect('coach_dashboard')
    if request.method == 'POST':
        form = PlayerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('coach_dashboard')
    else:
        form = PlayerProfileForm(instance=profile)
    return render(request, 'app/edit_player.html', {'form': form, 'profile': profile})

@user_passes_test(lambda u: u.is_coach())
def delete_player(request, player_id):
    profile = get_object_or_404(PlayerProfile, id=player_id)
    # Permite exclusão apenas se o jogador pertence a um time do coach
    if profile.team.coach != request.user:
        return redirect('coach_dashboard')
    if request.method == 'POST':
        user = profile.user
        profile.delete()
        user.delete()
        return redirect('coach_dashboard')
    return render(request, 'app/confirm_delete.html', {'profile': profile})

@login_required
@user_passes_test(lambda u: u.is_coach())
def create_player(request):
    if request.method == "POST":
        user_form = PlayerUserCreationForm(request.POST)
        profile_form = PlayerProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.role = 'player'
            user.set_password(user_form.cleaned_data['password1'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            # O coach deve escolher o time ao criar o jogador
            profile.save()
            return redirect('coach_dashboard')
    else:
        user_form = PlayerUserCreationForm(initial={'role': 'player'})
        profile_form = PlayerProfileForm()
    return render(request, 'app/create_player.html', {'user_form': user_form, 'profile_form': profile_form})
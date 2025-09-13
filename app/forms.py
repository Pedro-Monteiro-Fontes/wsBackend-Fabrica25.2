from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, PlayerProfile

class CoachUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email','role')  # role será 'coach' ao criar

class PlayerUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email','role')  # role setado para 'player'

class PlayerProfileForm(forms.ModelForm):
    class Meta:
        model = PlayerProfile
        fields = ('team','photo','points_per_game','assists','rebounds','minutes')


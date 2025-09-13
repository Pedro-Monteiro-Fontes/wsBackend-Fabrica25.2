from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    ROLE_CHOICES = (
        ('coach', 'Coach'),
        ('player', 'Player'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def is_coach(self):
        return self.role == 'coach'

    def is_player(self):
        return self.role == 'player'

class Team(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    coach = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              related_name='teams')

    def __str__(self):
        return self.name

class PlayerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
    photo = models.ImageField(upload_to='players/', blank=True, null=True)
    points_per_game = models.FloatField(default=0)
    assists = models.FloatField(default=0)
    rebounds = models.FloatField(default=0)
    minutes = models.FloatField(default=0)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.team.name}"
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, PlayerProfile, Team

@receiver(post_save, sender=User)
def create_profile_for_player(sender, instance, created, **kwargs):
    if created and instance.role == 'player':
        PlayerProfile.objects.create(user=instance, team=Team.objects.first() if Team.objects.exists() else None)

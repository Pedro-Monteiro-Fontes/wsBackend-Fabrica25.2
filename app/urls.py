from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('coach/', views.coach_dashboard, name='coach_dashboard'),
    path('player/', views.player_dashboard, name='player_dashboard'),
    path('team/<int:team_id>/add-player/', views.add_player, name='add_player'),
    path('player/<int:player_id>/edit/', views.edit_player_stats, name='edit_player'),
    path('player/<int:player_id>/delete/', views.delete_player, name='delete_player'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

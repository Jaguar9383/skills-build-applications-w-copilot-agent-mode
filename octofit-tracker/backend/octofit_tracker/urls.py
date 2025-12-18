"""octofit_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
import os

from octofit_tracker.views import UserViewSet, TeamViewSet, ActivityViewSet, WorkoutViewSet, LeaderboardViewSet, api_root

# Get codespace name from environment variable
CODESPACE_NAME = os.environ.get('CODESPACE_NAME')

# Determine the base URL
if CODESPACE_NAME:
    BASE_URL = f'https://{CODESPACE_NAME}-8000.app.github.dev'
else:
    BASE_URL = 'http://localhost:8000'

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'activities', ActivityViewSet)
router.register(r'workouts', WorkoutViewSet)
router.register(r'leaderboard', LeaderboardViewSet)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api_root, name='api-root'),
    path('', include(router.urls)),
]

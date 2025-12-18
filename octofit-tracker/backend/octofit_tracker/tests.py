
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from .models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone

class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        self.assertEqual(user.username, 'testuser')


class APITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='apitest', password='pass')
        self.client.force_authenticate(user=self.user)

    def test_api_root(self):
        response = self.client.get(reverse('api-root'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('users', response.data)

    def test_user_crud(self):
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, 200)

    def test_team_crud(self):
        team = Team.objects.create(name='API Team')
        team.members.add(self.user)
        response = self.client.get(reverse('team-list'))
        self.assertEqual(response.status_code, 200)

    def test_activity_crud(self):
        team = Team.objects.create(name='API Team')
        team.members.add(self.user)
        activity = Activity.objects.create(user=self.user, activity_type='Run', duration=20, calories_burned=100, date=timezone.now().date(), team=team)
        response = self.client.get(reverse('activity-list'))
        self.assertEqual(response.status_code, 200)

    def test_workout_crud(self):
        workout = Workout.objects.create(user=self.user, name='Situps', description='Do 30 situps')
        response = self.client.get(reverse('workout-list'))
        self.assertEqual(response.status_code, 200)

    def test_leaderboard_crud(self):
        team = Team.objects.create(name='API Team')
        leaderboard = Leaderboard.objects.create(team=team, total_points=50)
        response = self.client.get(reverse('leaderboard-list'))
        self.assertEqual(response.status_code, 200)

class TeamModelTest(TestCase):
    def test_create_team(self):
        user = User.objects.create_user(username='member', password='pass')
        team = Team.objects.create(name='Test Team')
        team.members.add(user)
        self.assertEqual(team.name, 'Test Team')
        self.assertIn(user, team.members.all())

class ActivityModelTest(TestCase):
    def test_create_activity(self):
        user = User.objects.create_user(username='activityuser', password='pass')
        activity = Activity.objects.create(user=user, activity_type='Run', duration=30, calories_burned=200, date=timezone.now().date())
        self.assertEqual(activity.activity_type, 'Run')

class WorkoutModelTest(TestCase):
    def test_create_workout(self):
        user = User.objects.create_user(username='workoutuser', password='pass')
        workout = Workout.objects.create(user=user, name='Pushups', description='Do 20 pushups')
        self.assertEqual(workout.name, 'Pushups')

class LeaderboardModelTest(TestCase):
    def test_create_leaderboard(self):
        team = Team.objects.create(name='Leaderboard Team')
        leaderboard = Leaderboard.objects.create(team=team, total_points=100)
        self.assertEqual(leaderboard.total_points, 100)

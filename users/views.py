from django.shortcuts import redirect
from django.http import JsonResponse
from django.views import View

from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import MyUser
import requests

import json

from deciduate.settings import GOOGLE_CLIENT_ID, GOOGLE_SECRET, REDIRECT_URI

class GoogleLoginView(View):
    def get(self, request):
        google_auth_url = (
            "https://accounts.google.com/o/oauth2/v2/auth"
            "?response_type=code"
            f"&client_id={GOOGLE_CLIENT_ID}"
            f"&redirect_uri={REDIRECT_URI}"
            "&scope=openid%20email%20profile"
        )
        return redirect(google_auth_url)

class GoogleCallbackView(View):
    def get(self, request):
        try:
            code = request.GET.get('code')
            token_response = requests.post(
                "https://oauth2.googleapis.com/token",
                data={
                    'code': code,
                    'client_id': GOOGLE_CLIENT_ID,
                    'client_secret': GOOGLE_SECRET,
                    'redirect_uri': REDIRECT_URI,
                    'grant_type': 'authorization_code',
                }
            )
            token_response_json = token_response.json()
            access_token = token_response_json.get('access_token')

            user_info_response = requests.get(
                'https://www.googleapis.com/oauth2/v2/userinfo',
                headers={'Authorization': f'Bearer {access_token}'}
            )
            user_info = user_info_response.json()

            email = user_info.get('email')
            user, created = MyUser.objects.get_or_create(email=email)
            if created:
                user.set_password(None)
                user.save()

            refresh = RefreshToken.for_user(user)
            login(request, user)
            return JsonResponse({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'email': email,
                'created': created
            }, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

class LogoutView(APIView):
    def post(self, request):
        try:
            logout(request)
            return JsonResponse({'message': 'Logged out successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

class RegisterView(APIView):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data['email']
            if MyUser.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email already exists'}, status=400)
            
            user = MyUser.objects.create_user(email=email)
            user.save()
            
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'email': email
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

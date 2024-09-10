import requests
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .models import YouTubeAccount
from .serializers import UserSerializer, YouTubeAccountSerializer

User = get_user_model()

class RegisterUser(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        
        email = request.data.get('email')
        first_name = request.data.get('first_name')
        username = request.data.get('username', None)  # Optional, as some users may not have a username
        access_token = request.data.get('access_token')

        if not email:
            return Response({'error': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)
        if not access_token:
            return Response({'error': 'Access token is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch YouTube data using the provided access token
        headers = {'Authorization': f'Bearer {access_token}'}
        print(headers)
        response = requests.get(
            "https://www.googleapis.com/youtube/v3/channels",
            params={
                'part': 'snippet,contentDetails,statistics',
                'mine': 'true'
            },
            headers=headers
        )

        if response.status_code != 200:
            return Response({'error': 'Failed to fetch YouTube data'}, status=status.HTTP_400_BAD_REQUEST)

        youtube_data = response.json().get('items', [])[0]  # Assuming the user has at least one YouTube channel

        youtube_account_data = {
            'youtube_id': youtube_data['id'],
            'youtube_etag': youtube_data['etag'],
            'youtube_title': youtube_data['snippet']['title'],
            'youtube_description': youtube_data['snippet'].get('description', ''),
            'youtube_custom_url': youtube_data['snippet'].get('customUrl', ''),
            'youtube_image': youtube_data['snippet']['thumbnails']['default']['url'],
        }

        user = User.objects.create_user(email=email, first_name=first_name, username=username)
        
        # Create YouTube account record and associate it with the user
        YouTubeAccount.objects.create(user=user, **youtube_account_data)
        
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

class UserDetails(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        user_data = UserSerializer(user).data
        return Response(user_data, status=status.HTTP_200_OK)

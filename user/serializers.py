from rest_framework import serializers
from .models import User, YouTubeAccount

class YouTubeAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = YouTubeAccount
        fields = ['id', 'youtube_id', 'youtube_etag', 'youtube_title', 'youtube_description', 'youtube_custom_url', 'youtube_image']

class UserSerializer(serializers.ModelSerializer):
    youtube_account = YouTubeAccountSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'about', 'is_staff', 'is_active', 'youtube_account']

    def create(self, validated_data):
        youtube_account_data = validated_data.pop('youtube_account', None)
        user = User.objects.create(**validated_data)
        
        if youtube_account_data:
            YouTubeAccount.objects.create(user=user, **youtube_account_data)
        
        return user

    def update(self, instance, validated_data):
        youtube_account_data = validated_data.pop('youtube_account', None)
        youtube_account = instance.youtube_account

        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.about = validated_data.get('about', instance.about)
        instance.save()

        if youtube_account_data:
            if youtube_account:
                # Update existing YouTube account
                youtube_account.youtube_id = youtube_account_data.get('youtube_id', youtube_account.youtube_id)
                youtube_account.youtube_etag = youtube_account_data.get('youtube_etag', youtube_account.youtube_etag)
                youtube_account.youtube_title = youtube_account_data.get('youtube_title', youtube_account.youtube_title)
                youtube_account.youtube_description = youtube_account_data.get('youtube_description', youtube_account.youtube_description)
                youtube_account.youtube_custom_url = youtube_account_data.get('youtube_custom_url', youtube_account.youtube_custom_url)
                youtube_account.youtube_image = youtube_account_data.get('youtube_image', youtube_account.youtube_image)
                youtube_account.save()
            else:
                # Create a new YouTube account
                YouTubeAccount.objects.create(user=instance, **youtube_account_data)

        return instance

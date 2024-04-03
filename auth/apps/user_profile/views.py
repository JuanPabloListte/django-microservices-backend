from rest_framework_api.views import StandardAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Profile
from .serializers import UserProfileSerializer
from django.contrib.auth import get_user_model
from django.core.cache import cache
import re
User = get_user_model()

pattern_special_characters = r'\badmin\b|[!@#$%^&*()_+-=[]{}|;:",.<>/?]|\s'

class MyUserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        if profile:
            serializer = UserProfileSerializer(profile)
            return self.send_response(serializer, status=status.HTTP_200_OK)
        else:
            return self.send_error('Profile not found', status=status.HTTP_404_NOT_FOUND)
        
class GetUserProfileView(StandardAPIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, slug, *args, **kwargs):
        print(slug)
        return self.send_response('profile_data')
    
class EditUsernameView(StandardAPIView):
    permissions_classes = (permissions.IsAuthenticated,)
    
    def put(self, request, format=None):
        data = self.request.data
        user = self.request.user
        user_model = User.objects.get(id=user.id)
        username = data['username']
        
        if re.search(pattern_special_characters,username, re.IGNORECASE) is None:
            user_model.username = username
            user_model.slug = username
            user_model.save()
            
            return self.send_response('Success',status=status.HTTP_200_OK)
        else:
            return self.send_error('Error',status.HTTP_400_BAD_REQUEST)
        
class GetUserProfileView(StandardAPIView):
    permissions_classes = (permissions.AllowAny,)
    
    def get(self, request, id, *args, **kwargs):
        cache_key = f'user_profile_{id}'
        profile_data = cache.get(cache_key)
        
        if not profile_data:
            user = User.objects.filter(id=id).first()
            if user:
                profile = Profile.objects.filter(user=user).first()
                if profile:
                    serializers = UserProfileSerializer(profile).data
                    profile_data = serializers
                    cache.set(cache_key, profile_data, 60 * 15)
                else:
                    return self.send_error("User profile not found", status_code=status.HTTP_404_NOT_FOUND)
            else: 
                return self.send_error("User not found", status_code=status.HTTP_404_NOT_FOUND)    
        return self.send_response(profile_data)
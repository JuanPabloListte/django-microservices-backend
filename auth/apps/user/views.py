from rest_framework_api.views import StandardAPIView
import json, uuid
from rest_framework import permissions, serializers, status
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from apps.user_profile.serializers import UserProfileSerializer
from apps.user_profile.models import Profile
from django.db import models
from django.core.cache import cache
User = get_user_model()


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return str(obj)
        return json.JSONEncoder.default(self, obj)
    
class ListAllUsersView(StandardAPIView):
    permissions_classes = (permissions.AllowAny,)
    def get(self, request, *args, **kwargs):
        user = User.objects.all()
        user_data = UserSerializer(user, many=True).data
        return self.paginate_response(request, json.dumps(user_data, cls=UUIDEncoder))

class GetUserView(StandardAPIView):
    permissions_classes = (permissions.AllowAny,)
    
    def get(self, request, id, *args, **kwargs):
        cache_key = f'user_{id}'
        user_data = cache.get(cache_key)
        
        if not user_data:
            user = User.objects.filter(id=id).first()
            if user:
                serializers = UserSerializer(user).data
                user_data = serializers
                cache.set(cache_key, user_data, 60 * 15)
            else:
                return self.send_error("User not found", status_code=status.HTTP_404_NOT_FOUND)
            
        return self.send_response(user_data)

class GetUserProfileSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='user.id')
    email = serializers.EmailField(source='user.email')
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    slug = serializers.CharField(source='user.slug')
    verified = serializers.BooleanField(source='user.verified')
    picture = serializers.ImageField(source='user.profile.picture')

    is_online = serializers.BooleanField(source='user.is_online')
    
    class Meta:
        model = Profile
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'slug', 'verified', 'picture', 'is_online']

class GetUserDetailsView(StandardAPIView):
    permissions_classes = (permissions.AllowAny,)
    def get(self, request, id, *args, **kwargs):
        user = User.objects.prefetch_related('profile', 'wallet').get(id=id)
        if user:
            serializer = UserProfileSerializer(user.profile)
            return self.send_response(serializer.data)
        else: 
            return self.send_error("User not found", status_code=status.HTTP_404_NOT_FOUND)
    

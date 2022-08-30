from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email',  'location', 'phone', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)


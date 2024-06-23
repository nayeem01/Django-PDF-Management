from rest_framework import serializers
from django.contrib.auth.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def save(self):
        if User.objects.filter(username=self.validated_data["username"]).exists():
            raise serializers.ValidationError({"username": "Username already exists"})

        user = User(username=self.validated_data["username"])
        password = self.validated_data["password"]
        user.set_password(password)
        user.save()
        return user

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


# Register
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "name", "password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


# Login
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(email=data["email"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Invalid credentials")

        refresh = RefreshToken.for_user(user)

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }


# Update
class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name"]


# Reset Password
class ResetPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):

        try:
            uid = force_str(urlsafe_base64_decode(data["uid"]))
            user = User.objects.get(id=uid)
        except:
            raise serializers.ValidationError("Invalid UID")

        if not PasswordResetTokenGenerator().check_token(user, data["token"]):
            raise serializers.ValidationError("Invalid or expired token")

        data["user"] = user
        return data

    def save(self):
        user = self.validated_data["user"]
        user.set_password(self.validated_data["password"])
        user.save()

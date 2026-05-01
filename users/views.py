from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .serializers import *

User = get_user_model()


class RegisterView(APIView):
    def post(self, request):
        s = RegisterSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        s.save()
        return Response({"msg": "Registered"})


class LoginView(APIView):
    def post(self, request):
        s = LoginSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        return Response(s.validated_data)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        token = RefreshToken(request.data["refresh"])
        token.blacklist()
        return Response({"msg": "Logged out"})


class UpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        s = UpdateSerializer(request.user, data=request.data, partial=True)
        s.is_valid(raise_exception=True)
        s.save()
        return Response(s.data)


class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get("email")
        user = User.objects.filter(email=email).first()

        if user:
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)

            print(f"/reset/{uid}/{token}/")  # replace with email send

        return Response({"msg": "If email exists, link sent"})


class ResetPasswordView(APIView):
    def post(self, request):
        s = ResetPasswordSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        s.save()
        return Response({"msg": "Password updated"})

from django.urls import path
from views import RegisterUser, LoginUser, LogoutUser, UserDetail, forgotPassword, resetPassword

urlpatterns = [
    path("/register", RegisterUser, name="register"),
    path("/login", LoginUser, name="login"),
    path("/logout", LogoutUser, name="logout"),
    path("/update-detail", UserDetail, name="update-detail"),
    path("/forgot-password", forgotPassword, name="forgot"),
    path("/reset-password", resetPassword, name="reset"),
]

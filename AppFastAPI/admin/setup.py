from sqladmin import Admin

from database import engine
from .views import RoleAdmin, UserAdmin
from .auth import AdminAuth


def setup_admin(app):
    admin = Admin(
        app,
        engine,
        authentication_backend=AdminAuth(secret_key="supersecret")
    )

    admin.add_view(RoleAdmin)
    admin.add_view(UserAdmin)

    return admin

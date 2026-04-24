from sqladmin.authentication import AuthenticationBackend
from fastapi import Request


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request):
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        if username == "admin" and password == "admin":
            request.session.update({"token": "admin"})
            return True
        return False

    async def logout(self, request: Request):
        request.session.clear()
        return True

    async def authenticate(self, request: Request):
        return request.session.get("token") == "admin"

from sqladmin import ModelView

from models.users import Role, User


class RoleAdmin(ModelView, model=Role):
    column_list = [Role.id, Role.name]
    column_searchable_list = [Role.name]


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.role]

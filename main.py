from fastapi import FastAPI
from database import session
from models import User
from sqlalchemy import and_, or_, not_
from sqlalchemy.orm.exc import UnmappedInstanceError

app = FastAPI()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # SQLAlchemy CRUD # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # ******************* CREATE ********************************
# user1 = User(name="Deep1", age=21)
# user2 = User(name="Deep2", age=22)
# user3 = User(name="Deep3", age=23)
# user4 = User(name="Deep4", age=24)
# user5 = User(name="Deep5", age=25)
# session.add_all([user1, user2, user3, user4, user5])
# session.commit()


# # ******************* READ ********************************
# # 1)
# # without all() queries would return SQL query.
# users = session.query(User).all()
# print("users: ", users)
# print(users[0].name)

# # 2)
# users_26 = session.query(User).filter_by(age=26).all()
# print("filter_by all: ", users_26)

# # 3)
# print("filter_by first: ", session.query(User).filter_by(age=26).first())

# # 4)
# print("filter_by one_or_none: ", session.query(User).filter_by(age=26).one_or_none())  # error if more then one


# # ******************* UPDATE ********************************
# user = session.query(User).first()
# user.name = "Changed Name"
# session.commit()

# # ******************* DELETE ********************************
# try:
#     user = session.query(User).filter_by(age=24).first()
#     session.delete(user)  # Will raise an error if user is None
#     session.commit()
#     print("User deleted successfully.")
# except UnmappedInstanceError:
#     print("User does not exist, nothing to delete.")


# # # # # # # # # # # # # # # # # # # # # # # # # # # # Order By Query # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# users = session.query(User).order_by(User.age, User.name).all()
# for user in users:
#   print("name: ", user.name, " age: ", user.age)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # Filter Query # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # 1) Filter (Supports multiple conditions with and_, or_, and operators like ==, <, >, in_, etc.)
# users = session.query(User).filter(User.age == 24).all()
# users = session.query(User).filter(User.age != 24).all()
# users = session.query(User).filter(User.name.like('%John%')).all()
# users = session.query(User).filter(User.age > 20, User.age < 30).all()
# users = session.query(User).filter(and_(User.age > 20, User.age < 30)).all()
# users = session.query(User).filter(or_(User.age > 20, User.name == 'deep1')).all()

# # # Combination of and_ , or_ , and not_
# complex_users = session.query(User).filter(or_(
#     and_(User.age == 25, User.name == "Deep5"),
#     not_(User.name == "Deep1")
# )).all()
# print("complex_users: ", complex_users)


# # # 2) Only supports = conditions (i.e., exact matches), Cannot use >, <, in_, or functions like like().
# users_26 = session.query(User).filter_by(age=25).all()
# print("filter_by age: ", users_26)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # Group By # # # # # # # # # # # # # # # # # # # # # # # # # # # #

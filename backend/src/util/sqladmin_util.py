from sqladmin import Admin, ModelView
from model.user.user_model import User
from model.restaurant.restaurant_model import Restaurant
from model.assignment.assignment_model import UserRestaurantAssignment
from fastapi import FastAPI
from db.session import engine


class UserAdmin(ModelView, model=User):
    column_list = [
      User.id, 
      User.email,
      User.name,
      User.is_active
    ]

class RestaurantAdmin(ModelView, model=Restaurant):
    column_list = [
        Restaurant.id,
        Restaurant.name,
        Restaurant.is_active,
        Restaurant.created_at,
        Restaurant.address,
        Restaurant.capacity
    ]

class AssignmentAdmin(ModelView, model=UserRestaurantAssignment):
    column_list = [
        UserRestaurantAssignment.id,
        UserRestaurantAssignment.user_id,
        UserRestaurantAssignment.restaurant_id,
        UserRestaurantAssignment.assignment_date,
        UserRestaurantAssignment.created_at
    ]

def set_admin(app: FastAPI):
    admin = Admin(app, engine)
    admin.add_view(UserAdmin)
    admin.add_view(RestaurantAdmin)
    admin.add_view(AssignmentAdmin)
from django.urls import path
from .views import *

urlpatterns = [
    path('Users/', AllUserList.as_view()),
    path('homepage/', index, name="index"),
    path('signup/', signup, name="addUserCol"),
    path('SignupAPI/', SignupAPI.as_view()),
    path('deleteUserByID/<int:uid>', DeleteUserByID.as_view()),
]

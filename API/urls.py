from django.urls import path
from .views import *

urlpatterns = [
    path('Users/', AllUserList.as_view()),
    path('homepage/', index, name="index"),
    path('signup/', signup, name="signup")
]

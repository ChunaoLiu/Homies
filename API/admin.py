from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(User)
class UserModel(admin.ModelAdmin):
    list_filter = ('name', 'email')
    list_display = ('name', 'email')

@admin.register(Dorm)
class DormModel(admin.ModelAdmin):
    list_filter = ('Dorm_id', 'num_ppl')
    list_display = ('Dorm_id', 'num_ppl')
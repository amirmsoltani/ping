from django.contrib import admin
from .models import *


admin.site.register(Member)
admin.site.register(Message)
admin.site.register(Connection)
admin.site.register(Category)
from django.contrib import admin
from .models import Client , Hotel,Rating

admin.site.register([Client,Hotel,Rating])

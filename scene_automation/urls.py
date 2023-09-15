from django.contrib import admin
from django.urls import path
from front_end.views import say_hello

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', say_hello, name='say_hello')
]

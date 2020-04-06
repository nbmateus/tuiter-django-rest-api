from django.contrib import admin
from django.urls import path, include
from .views import tuiterAPIRootView

urlpatterns = [
    path('',tuiterAPIRootView),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('postings/', include('postings.urls')),
]

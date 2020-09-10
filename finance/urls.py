
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', include("accounts.urls", namespace="accounts")),
    path('inflow/', include("inflow.urls", namespace="inflow")),
    path('outflow/', include("outflow.urls", namespace="outflow")),
]

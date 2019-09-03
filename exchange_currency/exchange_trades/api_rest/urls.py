
from django.urls import path, include

from .v1.routers import api_urlpatterns as api_v1
# solo ejemplo
# from .api.v2.router import api_urlpatterns as api_v2

urlpatterns = [
    # ^api/',
    path(r'v1/', include(api_v1)),
]

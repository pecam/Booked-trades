from django.urls import path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

api_urlpatterns = [
    path(r'currency_list/', views.TradesListWS.as_view()),
    path(r'new_trade/<str:sell_currency>/<sell_amount>/<buy_currency>/<buy_amount>/<rate>', views.NewTradeWS.as_view()), #method put
    path(r'new_trade/', views.NewTradeWS.as_view()), # method get
    path(r'get_rate/', views.FixerExchangeWS.as_view()),
]

api_urlpatterns += router.urls
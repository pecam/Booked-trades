import datetime
from decimal import Decimal
from django.http import HttpResponse, JsonResponse
import json
import requests
from rest_framework import status

from exchange_trades.api_rest import ResourceAPIRest
from exchange_trades.models import ExchangeTrades, Currency
from exchange_trades.fixer import Fixer


class TradesListWS(ResourceAPIRest):
    group = 'Currency'
    name =  'TradesList'
    code = 'TradesList'

    def get(self, request, *args, **kwargs):
        data = ExchangeTrades.objects.all().values(
                'identifier', 'sell_currency__code', 'sell_amount', 
                'buy_currency__code', 'buy_amount', 'rate', 'date_booked').order_by('-date_booked')
        return JsonResponse({'results': list(data)})


class NewTradeWS(ResourceAPIRest):
    """ Create new trade """
    group = 'Currency'
    name = 'Newtrade'
    code = 'Newtrade'


    def get(self, request, *arg, **kwargs):
        '''
        Example: http://127.0.0.1:8000/api/v1/new_trade/?sell_currency=2&sell_amount=500&buy_currency=2&buy_amount=600&rate=45455
        '''
        data = request.GET.copy() or {}
        sell_currency = Currency.objects.get(code=data.get('sell_currency'))
        sell_amount=Decimal(data.get('sell_amount'))
        buy_currency= Currency.objects.get(code=data.get('buy_currency'))
        buy_amount= data.get('buy_amount')
        
        try:
            ExchangeTrades.objects.create(
                sell_currency=sell_currency, 
                sell_amount=sell_amount,
                buy_currency=buy_currency,
                buy_amount=buy_amount,
                rate=Decimal(data.get('rate')),
                date_booked=datetime.date.today()
                )
        except Exception as e:
            res = {'ERROR': ["Error in create object ExchangeTrades"]}
            raise "Error create object"


        res = {'SUCCESS': ['Todo ok']}
        res = json.dumps(res)
        return HttpResponse(res, content_type='application/json', status=status.HTTP_200_OK)
 
    
    def put(self, request, sell_currency, sell_amount, buy_currency, buy_amount, rate, *arg, **kwargs):
        """
        Example: http://127.0.0.1:8000/api/v1/new_trade/EUR/100/USD/109.68500000000002/1.09685
        """
        # import pdb; pdb.set_trace()
        sell_currency = Currency.objects.get(code=sell_currency)
        buy_currency= Currency.objects.get(code=buy_currency)
        
        # TODO: SECURITY: CHECK BUY AMOUNT DONT HAVE BEEN MODIFY
        # sell_amount = Decimal(sell_amount.replace(',',''))
        # rate = Decimal(rate.replace(',',''))
        # buy_amount_security = round(sell_amount * rate, 2)
        #if buy_amount_security != buy_amount:
        #    return {'ERROR': ["Buy amount have been modify"]}

        try:
            ExchangeTrades.objects.create(
                sell_currency=sell_currency, 
                sell_amount=sell_amount,
                buy_currency=buy_currency,
                buy_amount=buy_amount,
                rate=rate,
                date_booked=datetime.date.today()
                )

        except Exception as e:
            # log.err(e)
            res = {'ERROR': ["Error in create object ExchangeTrades"]}
            raise "Error create object"


        res = {'SUCCESS': ['Todo ok']}
        res = json.dumps(res)
        return HttpResponse(res, content_type='application/json', status=status.HTTP_200_OK)


class FixerExchangeWS(ResourceAPIRest):
    group = 'Exchange'
    name = 'FixerExchange'
    code = 'FixerExchange'

    def get(self, request, *arg, **kwargs):
        # http://127.0.0.1:8000/api/v1/get_rate/?base=EUR&symbols=USD
        # import pdb; pdb.set_trace()
        data = request.GET.copy() or {}
        base = data.get('base')
        symbols = data.get('symbols')
        #check symbols is a str
        if not isinstance(symbols, str):
            raise ValueError('symbols params is not string')  # I know symbols can be list but i dont want used

        fixer_api = Fixer()
        change = fixer_api.get_exchange(base, symbols)
        return HttpResponse(json.dumps(change), content_type='application/json', status=status.HTTP_200_OK)


from django.db import models
import uuid
import json

class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=20, db_index=True)

    def __str__(self):
        return self.code


class ExchangeTrades(models.Model):
    identifier = models.CharField(max_length=9, db_index=True, unique=True)
    sell_currency = models.ForeignKey(Currency, related_name='currency_sell', on_delete=models.CASCADE)
    sell_amount = models.DecimalField(db_index=True, decimal_places=2, max_digits=18)
    buy_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='currency_buy')
    buy_amount = models.DecimalField(db_index=True, decimal_places=2, max_digits=18)
    rate = models.DecimalField(db_index=True, decimal_places=4, max_digits=18)
    date_booked =  models.DateField(verbose_name='Date booked')
    
    def save(self, *args, **kwargs):
        if not self.identifier:
            self.identifier = self.id_generator()
            while ExchangeTrades.objects.filter(identifier=self.identifier).exists():
                self.identifier = self.id_generator()
        super().save(*args, **kwargs)
    
    @property
    def parsed_data(self):
        return {
            'identifier': self.identifier,
            'sell_currency': self.sell_currency,
            'sell_amount': self.sell_amount,
            'buy_currency': self.buy_currency,
            'buy_amount': self.buy_amount,
            'rate': str(self.rate),
            'date_booked': str(self.date_booked),
        }

    def toJSON(self):
        return json.dumps(self.parsed_data)

    def id_generator(self):
        """ Random identifier generator

        Identifier unique with formar: TR + 7 alphanumerics

        Retuns:
           random_id (str)

        """

        random_id = uuid.uuid4().hex[:7].upper()
        random_id = "TR" + random_id
        return random_id

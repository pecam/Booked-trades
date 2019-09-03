from django.conf import settings
import json
import requests


class Fixer(object):
    """ Manager to connect Fixer.io (exchange rate data sources) """

    url = getattr(settings, 'FIXER_URL', 'http://data.fixer.io/api/latest')
    access_key = getattr(settings, 'FIXER_ACCESS_KEY', '782e738abe9187b1f8c55d4a275472d9')
    url_symbols = "https://data.fixer.io/api/symbols"

    def get_url(self, base, symbols):
        """ Replace url with get params

        Args:
            base (str): sell currency
            symbols (str): buy currency

        Returns:
            url (str): api url 
        """
        url = self.url + "?access_key=" + self.access_key + "&base=" + base + "&symbols=" + symbols
        return url

    def get_url_symbols(self):
        url = self.url_symbols + "?access_key=" + self.access_key
        return url

    def parse_json(self, response):  # TODO: doc
        if isinstance(response, bytes):
            response = response.decode("utf-8")
        #return json.loads(response, parse_float=Decimal)
        return json.loads(response)

    def get_response(self, url=None, **params):
        url = url if url else self.get_url(**params)
        return requests.get(url)

    def parse_response(self, response):
        data = self.parse_json(response.text)
        return data

    def get_exchange(self, base, symbols):
        """ Return rate exchange currency

        Args:
            base (str): sell currency
            symbols (str): buy currency

        Returns:
            rates (str): json string  # TODO: 

        Raises:
            ValueError: If base param or symbols param is null

        Examples: 
            http://data.fixer.io/api/latest?access_key=782e738abe9187b1f8c55d4a275472d9&base=EUR&symbols=USD
            {
                "success": true,
                "timestamp": 1567185486,
                "base": "EUR",
                "date": "2019-08-30",
                "rates": {"USD": 1.097984}
            }
        """

        if not base or not symbols:
            raise ValueError('base param or symbols param is null')

        url = self.get_url(base=base, symbols=symbols)
        response = self.get_response(url=url)

        parsed_response = self.parse_response(response)
        if parsed_response.get('success') == False:
            # {'success': False, 'error': {'code': 105, 'type': 'base_currency_access_restricted'}}
            return {
                    'success': False, 
                    'error': parsed_response['error']['type'],
            }

        parsed_response = {
            'success': parsed_response.get('success'),
            'error': '',
            'rates': parsed_response['rates'][symbols]
        }
        return parsed_response


    def get_symbols(self):
        """
        Get symbols to import in database
        
        TODO: Access Restricted

        Returns:
        {
            'success': False, 
            'error': {
                'code': 105, 
                'type': 'https_access_restricted', 
                'info': 'Access Restricted - Your current Subscription Plan does not support HTTPS Encryption.'
            }
        }
        """
        url = self.get_url_symbols()
        response = self.get_response(url=url)
        parsed_response = self.parse_response(response)
        return parsed_response



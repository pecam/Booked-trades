pip install -r requirements.txt
sudo npm install @vue/cli
sudo npm install bootstrap-vue
sudo npm install axios
sudo npm install sweetalert
python exchange_currency/manage.py migrate
python exchange_currency/manage.py createsuperuser
python exchange_currency/manage.py loaddata data/currency.json
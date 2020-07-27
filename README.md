# SbWatcher
Разрабатывается силами Python 3.8 будет работать на Python 3.2. Зато дешево. 

Используюстся следующие файлы
 - `request.py` - скрипт для получения информации
 - `report.py` - скрипт для отправки отчётов
 - `analize.py` - скрипт для анализа полученной информации и формирования отчётов

```
https://www.sberbank.ru/portalserver/proxy/?pipe=shortCachePipe&url=http%3A%2F%2Flocalhost%2Frates-web%2FrateService%2Frate%2Fcurrent%3FregionId%3D77%26rateCategory%3Dbeznal%26currencyCode%3DA33%26currencyCode%3DA76%26currencyCode%3DA98%26currencyCode%3DA99
```
```
https://www.sberbank.ru/portalserver/proxy/?pipe=shortCachePipe&url=http://localhost/rates-web/rateService/rate/current?regionId=77&rateCategory=beznal&currencyCode=A33&currencyCode=A76&currencyCode=A98&currencyCode=A99
```

```JavaScript
{'beznal': 
    {'840': 
        {'0': 
            {'isoCur': 'USD', 'currencyName': 'Доллар США', 'currencyNameEng': 'US Dollar', 'rateType': 'CURRENCY', 'categoryCode': 'beznal', 'scale': 1, 'buyValue': 70.18, 'sellValue': 73.32, 'activeFrom': 1595809322000, 'buyValuePrev': 70.16, 'sellValuePrev': 73.18, 'amountFrom': 0, 'amountTo': 9999999999.99}
        }, 
    'A99': 
        {'0': 
            {'isoCur': 'Silver', 'currencyName': 'Серебро', 'currencyNameEng': 'Silver', 'rateType': 'METAL', 'categoryCode': 'beznal', 'scale': 1, 'buyValue': 52.98, 'sellValue': 57.98, 'activeFrom': 1595819707000, 'buyValuePrev': 51.98, 'sellValuePrev': 56.97, 'amountFrom': 0, 'amountTo': 9999999999.99}
        }, 
    'A33': 
        {'0': 
            {'isoCur': 'palladium', 'currencyName': 'Палладий', 'currencyNameEng': 'Palladium', 'rateType': 'METAL', 'categoryCode': 'beznal', 'scale': 1, 'buyValue': 4832, 'sellValue': 5459, 'activeFrom': 1595819707000, 'buyValuePrev': 4821, 'sellValuePrev': 5447, 'amountFrom': 0, 'amountTo': 9999999999.99}
        }
    }
}
```

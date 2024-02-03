import platform
import aiohttp
import asyncio
from datetime import datetime, timedelta
import sys
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(funcName)5s - %(message)s")


async def exchange_rate(banks_api):

    try:
        async with aiohttp.ClientSession() as session:

            async with session.get(banks_api) as response:
                if response.status == 200:
                    logging.info(f"Status: {response.status}")
                    return await response.json()
    except ConnectionError as e:
        logging.info(f"Status: {response.status}")
        logging.error(f"Error: {e}")


async def extractor(data, currency, operation) -> int:

    try:
        return list(filter(lambda sale: sale.get('currency') == currency, data.get('exchangeRate')))[0].get(operation)
    except IndexError:
        # print("Bank not yet to formed exchange Rate")
        return []


async def collector(data, currency_: set) -> dict:

    ext_dict = {
        data.get('date'): {
            currency: {
                'sale': await extractor(data, currency, 'saleRate'),
                'purchase': await extractor(data, currency, 'purchaseRate')
            }
            for currency in currency_
        }
    }

    return ext_dict


async def delta_days(days) -> list:

    days_list = []
    now = datetime.now()
    if 1 <= days <= 10:
        days_list.append(now.strftime("%d.%m.%Y"))
        if 1 < days <= 10:
           for i in range(days - 1):
                now = now - timedelta(days=1)
                days_list.append(now.strftime("%d.%m.%Y"))
        return days_list
    else:
        logging.error(f"ValueError days: {days} (range must be 1 to 10)")
        return []


async def main(currency: set, days=1) -> list:

    result = []
    days_range = await delta_days(days)

    for i in days_range:
        banks_api = ''.join(['https://api.privatbank.ua/p24api/exchange_rates?json&date=', i])
        result.append(await collector(await exchange_rate(banks_api), currency))
    return result

if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    currency_set = {'EUR', 'USD'}
    compare_currency = ('EUR', 'USD', 'CHF', 'GBP', 'PLZ', 'SEK', 'CAD')

    if len(sys.argv) > 2:
        for p in sys.argv[2:]:
            if p.upper() in compare_currency:
                currency_set.add(p.upper())
        print(currency_set)

    if len(sys.argv) > 1:
        r = asyncio.run(main(currency=currency_set, days=int(sys.argv[1])))
        print(r)
    else:
        r = asyncio.run(main(currency=currency_set))
        print(r)


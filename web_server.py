import asyncio
import logging

import websockets
import names
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK
from aiofile import async_open
from aiopath import AsyncPath

from main import main

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(funcName)5s - %(message)s")


async def forma(data: list) -> str:
    days_list = []

    for item in data:
        for date, currencies in item.items():
            cur_list = []
            dt = f"Date: {date}"
            for currency, values in currencies.items():
                cur_srt = f"{currency} -> Sale: {values['sale']} Purchase: {values['purchase']}\n"
                cur_list.append(cur_srt)
            day = f"{dt}\n{''.join(cur_list)}"
            days_list.append(day)

    return "\n".join(days_list)


async def currency_log(data: list):
    log_file = AsyncPath("currency_log.txt")

    if await log_file.exists():
        async with async_open("currency_log", 'w') as fh:
            await fh.write(f"{await forma(data)}\n")
    else:
        async with async_open("currency_log", 'a') as fh:
            await fh.write(f"{await forma(data)}\n")


async def request(message: str) -> str:
    days = 1
    currency_set = {'EUR', 'USD'}
    compare_currency = ('EUR', 'USD', 'CHF', 'GBP', 'PLZ', 'SEK', 'CAD')
    p = message.split(' ')
    for i in p:
        if i.upper() in compare_currency:
            currency_set.add(i.upper())
        if i.isdigit():
            days = int(i)
    result = await main(currency=currency_set, days=days)
    try:
        await currency_log(result)
    except Exception as e:
        logging.error(e)
    return await forma(result)


class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        ws.name = names.get_full_name()
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects')

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects')

    async def send_to_clients(self, message: str):
        if self.clients:
            [await client.send(message) for client in self.clients]

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distrubute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def distrubute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            if message.startswith("exchange"):
                exchange = await request(message)
                await self.send_to_clients(exchange)
            elif message.lower() == 'hello server':
                await self.send_to_clients("Server: Hello, glad to see you!")
            else:
                await self.send_to_clients(f"{ws.name}: {message}")


async def run_serv():
    server = Server()
    async with websockets.serve(server.ws_handler, 'localhost', 8080):
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    asyncio.run(run_serv())

import logging
from typing import List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import asyncio

from publisher import Publisher
from consumer import Consumer

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_json(message)


manager = ConnectionManager()

cmd_publisher = Publisher('cmd')
# cmd_publisher.send_msg('init')

# logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
# amqp_url = 'amqp://guest:guest@localhost:5672/%2F'
# consumer = ReconnectingConsumer(amqp_url, 'cmd')
# consumer.run()

async def send_ws(message):
    logging.debug(f'WS-manager got message {message}')
    print(message)
    await manager.broadcast(message)



app = FastAPI()
# https://stackoverflow.com/questions/65586853/how-to-use-fastapi-as-consumer-for-rabbitmq-rpc
@app.on_event('startup')
async def startup():
    loop = asyncio.get_event_loop()
    # use the same loop to consume
    # asyncio.ensure_future(consume(loop))
    data_consumer = Consumer('data', loop, send_ws)
    cmd_consumer = Consumer('cmd', loop, send_ws)
    # asyncio.ensure_future(consumer.run())
    await data_consumer.run()
    await cmd_consumer.run()

@app.get("/")
async def get():
    # cmd_publisher.send_msg('start')
    return {"message": "start sent"}


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # await manager.send_personal_message(f"You wrote: {data}", websocket)
            # await manager.broadcast(f"Client #{client_id} says: {data}")

            # decode message
            cmd_publisher.send_msg(data)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
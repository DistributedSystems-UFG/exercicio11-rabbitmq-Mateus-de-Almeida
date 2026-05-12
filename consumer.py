import asyncio
import sys
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import rabbitpy
import time
from const import *

# Consumidor simples: lê continuamente da fila de comidas (cozinha)
print('[Cozinha] Aguardando pedidos de comida...')

with rabbitpy.Connection(f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_ADDR}:5672/{RABBITMQ_VHOST}') as conn:
    with conn.channel() as channel:
        queue = rabbitpy.Queue(channel, QUEUE_COMIDA, durable=True, auto_delete=False)
        queue.declare()

        for message in queue:
            pedido = message.body.decode()
            print(f'[Cozinha] Preparando: {pedido}')
            time.sleep(2)  # simula tempo de preparo
            print(f'[Cozinha] Pronto: {pedido}')
            message.ack()

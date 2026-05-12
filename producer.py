import asyncio
import sys
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import rabbitpy
from const import *

# Simula um cliente fazendo um pedido simples (comida + bebida + pagamento)
cliente = 'Mesa 1'

with rabbitpy.Connection(f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_ADDR}:5672/{RABBITMQ_VHOST}') as conn:
    with conn.channel() as channel:

        exchange = rabbitpy.Exchange(channel, EXCHANGE)
        exchange.declare()

        for queue_name, key in [(QUEUE_COMIDA, KEY_COMIDA),
                                (QUEUE_BEBIDA, KEY_BEBIDA),
                                (QUEUE_CAIXA,  KEY_CAIXA)]:
            q = rabbitpy.Queue(channel, queue_name, durable=True, auto_delete=False)
            q.declare()
            q.bind(exchange, key)

        pedidos = [
            (KEY_COMIDA, f'{cliente}: X-Burguer'),
            (KEY_BEBIDA, f'{cliente}: Suco de Laranja'),
            (KEY_CAIXA,  f'{cliente}: R$ 35,00'),
        ]

        for routing_key, corpo in pedidos:
            msg = rabbitpy.Message(channel, corpo)
            msg.publish(exchange, routing_key)
            print(f'[Produtor] Enviado -> {corpo}')

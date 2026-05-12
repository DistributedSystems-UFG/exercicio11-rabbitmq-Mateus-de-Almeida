import asyncio
import sys
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import rabbitpy
from const import *

# Cada entrada representa um cliente/mesa com seus pedidos
CLIENTES = [
    {
        'mesa': 'Mesa 2',
        'pedidos': [
            (KEY_COMIDA, 'Mesa 2: Frango Grelhado'),
            (KEY_BEBIDA, 'Mesa 2: Refrigerante'),
            (KEY_CAIXA,  'Mesa 2: R$ 28,00'),
        ]
    },
    {
        'mesa': 'Mesa 3',
        'pedidos': [
            (KEY_COMIDA, 'Mesa 3: Batata Frita'),
            (KEY_COMIDA, 'Mesa 3: Salada Caesar'),
            (KEY_BEBIDA, 'Mesa 3: Agua com Gas'),
            (KEY_CAIXA,  'Mesa 3: R$ 42,00'),
        ]
    },
    {
        'mesa': 'Mesa 4',
        'pedidos': [
            (KEY_BEBIDA, 'Mesa 4: Vitamina de Banana'),
            (KEY_CAIXA,  'Mesa 4: R$ 12,00'),
        ]
    },
]

def setup_infra(channel):
    exchange = rabbitpy.Exchange(channel, EXCHANGE)
    exchange.declare()
    for queue_name, key in [(QUEUE_COMIDA, KEY_COMIDA),
                            (QUEUE_BEBIDA, KEY_BEBIDA),
                            (QUEUE_CAIXA,  KEY_CAIXA)]:
        q = rabbitpy.Queue(channel, queue_name, durable=True, auto_delete=False)
        q.declare()
        q.bind(exchange, key)
    return exchange

def producer():
    connection = rabbitpy.Connection(f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_ADDR}:5672/{RABBITMQ_VHOST}')
    channel = connection.channel()
    exchange = setup_infra(channel)

    for cliente in CLIENTES:
        print(f'\n[Produtor] Enviando pedidos da {cliente["mesa"]}...')
        for routing_key, corpo in cliente['pedidos']:
            msg = rabbitpy.Message(channel, corpo)
            msg.publish(exchange, routing_key)
            print(f'  -> {corpo}')

    connection.close()

if __name__ == '__main__':
    producer()

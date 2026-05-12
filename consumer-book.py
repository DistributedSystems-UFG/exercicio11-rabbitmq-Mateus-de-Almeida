import asyncio
import sys
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import rabbitpy
import time
import threading
from const import *

# Cada consumidor representa uma estação da lanchonete

def cozinha():
    """Consome pedidos de comida e simula o preparo."""
    conn = rabbitpy.Connection(f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_ADDR}:5672/{RABBITMQ_VHOST}')
    channel = conn.channel()
    queue = rabbitpy.Queue(channel, QUEUE_COMIDA, durable=True, auto_delete=False)
    queue.declare()

    while len(queue) > 0:
        msg = queue.get()
        pedido = msg.body.decode()
        print(f'[Cozinha]  Preparando -> {pedido}')
        time.sleep(1)
        print(f'[Cozinha]  Entregue  -> {pedido}')
        msg.ack()

    conn.close()

def bar():
    """Consome pedidos de bebida e simula o preparo."""
    conn = rabbitpy.Connection(f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_ADDR}:5672/{RABBITMQ_VHOST}')
    channel = conn.channel()
    queue = rabbitpy.Queue(channel, QUEUE_BEBIDA, durable=True, auto_delete=False)
    queue.declare()

    while len(queue) > 0:
        msg = queue.get()
        pedido = msg.body.decode()
        print(f'[Bar]      Preparando -> {pedido}')
        time.sleep(1)
        print(f'[Bar]      Entregue  -> {pedido}')
        msg.ack()

    conn.close()

def caixa():
    """Consome registros de pagamento e imprime o recibo."""
    conn = rabbitpy.Connection(f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_ADDR}:5672/{RABBITMQ_VHOST}')
    channel = conn.channel()
    queue = rabbitpy.Queue(channel, QUEUE_CAIXA, durable=True, auto_delete=False)
    queue.declare()

    while len(queue) > 0:
        msg = queue.get()
        pagamento = msg.body.decode()
        print(f'[Caixa]    Recibo emitido -> {pagamento}')
        msg.ack()

    conn.close()

def consumer():
    threads = [
        threading.Thread(target=cozinha, name='Cozinha'),
        threading.Thread(target=bar,     name='Bar'),
        threading.Thread(target=caixa,   name='Caixa'),
    ]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print('\n[Sistema] Todos os pedidos foram processados.')

if __name__ == '__main__':
    consumer()

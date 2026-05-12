# RabbitMQ — Sistema de Pedidos de Lanchonete

Exemplo produtor-consumidor com RabbitMQ usando Python (`rabbitpy`).  
Tema: pedidos de uma lanchonete roteados para três filas (Cozinha, Bar, Caixa).

---

## Arquitetura

```
[producer.py / producer-book.py]
                  |
          Exchange: lanchonete
         /          |          \
pedido.comida  pedido.bebida  pedido.caixa
      |              |              |
[QUEUE_COMIDA] [QUEUE_BEBIDA]  [QUEUE_CAIXA]
      |              |              |
  [Cozinha]        [Bar]         [Caixa]
        \            |            /
         [consumer.py / consumer-book.py]
```

---

## Pré-requisitos (Windows)

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado e rodando
- Python 3 com `rabbitpy`:
  ```
  pip install rabbitpy
  ```

---

## 1. Subir o RabbitMQ via Docker

Execute **uma única vez** no PowerShell ou CMD:

```powershell
docker run -d --name rabbitmq ^
  -p 5672:5672 -p 15672:15672 ^
  rabbitmq:3-management
```

Criar o usuário e o vhost:

```powershell
docker exec rabbitmq rabbitmqctl add_user myuser abc123
docker exec rabbitmq rabbitmqctl add_vhost my_vhost
docker exec rabbitmq rabbitmqctl set_permissions -p my_vhost myuser ".*" ".*" ".*"
```

---

## 2. Configuração

Edite `const.py` se necessário (padrão já aponta para `localhost`).

---

## 3. Executar

**Terminal 1 — Consumidor:**
```
python consumer.py
```

**Terminal 2 — Produtor:**
```
python producer.py
```

**Terminal 3 — Produtores (Mesas 2, 3 e 4):**
```
python producer-book.py
```

**Terminal 4 — Consumidores (Cozinha, Bar e Caixa em paralelo):**
```
python consumer-book.py
```

---

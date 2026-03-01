# Деплой на Yandex Cloud

## Варианты размещения

1. **Serverless Containers** — контейнер по запросу, оплата за использование.
2. **Compute Cloud (VM)** — виртуальная машина с Docker.
3. **Managed Service for Kubernetes** — если нужна оркестрация.

Ниже — общие шаги для контейнера (Registry + Serverless Containers или VM).

---

## 1. Сборка и проверка образа локально

```bash
docker build -t vibe-flask .
docker run -p 8080:8080 -e SECRET_KEY=test -e FLASK_ENV=production vibe-flask
# Проверка: http://localhost:8080/ и http://localhost:8080/health
```

---

## 2. Yandex Container Registry

1. В консоли Yandex Cloud: **Container Registry** → создать реестр и репозиторий.
2. Установить [Yandex Cloud CLI](https://cloud.yandex.ru/docs/cli/quickstart) и авторизоваться:
   ```bash
   yc init
   yc container registry configure-docker
   ```
3. Собрать образ с тегом реестра (подставьте свой `cr.xxx.yandex/xxx/vibe-flask`):
   ```bash
   docker build -t cr.yandex/<registry-id>/vibe-flask:latest .
   docker push cr.yandex/<registry-id>/vibe-flask:latest
   ```

---

## 3. Serverless Containers

1. **Serverless Containers** → создать контейнер.
2. Указать образ из Registry: `cr.yandex/<registry-id>/vibe-flask:latest`.
3. Ресурсы: 0.5–1 vCPU, 512 MB–1 GB RAM (по нагрузке).
4. Переменные окружения: `SECRET_KEY`, `FLASK_ENV=production`, при необходимости `DATABASE_URL`.
5. Порт контейнера: **8080** (уже задан в Dockerfile).
6. Health check: путь **/health**, порт 8080.
7. Создать триггер (HTTP) и получить URL.

---

## 4. Compute Cloud (VM)

1. Создать VM (Ubuntu 22.04).
2. Установить Docker, авторизоваться в Registry:
   ```bash
   yc container registry configure-docker
   ```
3. Запустить контейнер (подставьте свой образ и секреты):
   ```bash
   docker run -d --restart unless-stopped \
     -p 8080:8080 \
     -e SECRET_KEY="ваш-секрет" \
     -e FLASK_ENV=production \
     --name vibe-flask \
     cr.yandex/<registry-id>/vibe-flask:latest
   ```
4. Настроить Application Load Balancer или открыть порт в группе безопасности.

---

## 5. Переменные окружения (production)

| Переменная       | Описание |
|------------------|----------|
| `SECRET_KEY`     | Секретный ключ Flask (обязательно сменить). |
| `FLASK_ENV`      | `production` для продакшена. |
| `DATABASE_URL`   | При использовании Managed Service for PostgreSQL. |
| `PORT`           | Обычно 8080; в Serverless Containers задаётся платформой. |

См. также `.env.example` в корне проекта.

---

## 6. База данных (опционально)

Для **Managed Service for PostgreSQL** укажите в конфиге подключение в формате:

```
postgresql://user:password@host:6432/dbname?sslmode=require
```

И добавьте в `requirements.txt`: `psycopg2-binary` или `asyncpg` при необходимости.

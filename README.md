# Vibe Flask

Мой **вайбкодинг пет-проект** — небольшой сайт на Flask.

## Что внутри

- **Обо мне** — страница-визитка
- **Котировки** — обновляемые котировки Сбера и Совкомбанка с [MOEX ISS API](https://iss.moex.com/)
- **Блог** — список постов и страницы статей
- **О проекте** — краткое описание для гостей и GitHub

Сборка под хостинг в **Yandex Cloud** (Docker, Container Registry, Serverless Containers).

## Стек

- Python 3.12, Flask, Gunicorn
- Jinja2, CSS/JS
- MOEX ISS API для котировок

## Запуск локально

```bash
pip install -r requirements.txt
cp .env.example .env   # при необходимости
python run.py
```

Сайт: http://127.0.0.1:5000

## Деплой (Yandex Cloud)

См. [deploy/YANDEX.md](deploy/YANDEX.md).

```bash
docker build -t vibe-flask .
docker run -p 8080:8080 -e SECRET_KEY=... -e FLASK_ENV=production vibe-flask
```

---

Pet project, vibe coding.

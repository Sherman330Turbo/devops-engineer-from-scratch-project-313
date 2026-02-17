## Деплой приложения на PaaS (DevOps)

### Hexlet project

[![Actions Status](https://github.com/Sherman330Turbo/devops-engineer-from-scratch-project-313/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Sherman330Turbo/devops-engineer-from-scratch-project-313/actions)
[![main](https://github.com/Sherman330Turbo/devops-engineer-from-scratch-project-313/actions/workflows/main.yml/badge.svg)](https://github.com/Sherman330Turbo/devops-engineer-from-scratch-project-313/actions/workflows/main.yml)

Учебный DevOps-проект на Python. Представляет собой сервис сокращения ссылок с полноценным CRUD-бэкендом. Проект
предназначен для практики CI/CD, контейнеризации и воспроизводимого локального запуска через `make`.

---

## Архитектура проекта

1. **Backend** — Flask-приложение с CRUD-логикой сокращателя ссылок.
2. **Frontend** — подключается как внешняя npm-зависимость.
3. **Инфраструктура**:
    - единый Docker-образ;
    - Nginx в роли reverse proxy;
    - сборка фронтенда и бэкенда внутри контейнера.

Контейнер запускает backend и Nginx, который:

- проксирует API-запросы к приложению;
- отдаёт собранную статику фронтенда.

---

## Деплой

Приложение доступно по адресу:

https://devops-engineer-from-scratch-project-313-1rpc.onrender.com/

---

## Доступные команды

```bash
# Запуск локального development-сервера
uv run make start

# Установка всех зависимостей (backend + frontend)
uv run make install

# Линтинг
uv run make lint

# Тестирование
uv run make test

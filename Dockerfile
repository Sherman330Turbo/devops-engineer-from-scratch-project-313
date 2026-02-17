# Собираем фронтовый образ
FROM node:20-alpine AS front-build

WORKDIR /

COPY package.json package-lock.json /

RUN npm ci

FROM python:3.14.3-slim-bookworm AS runtime-build

WORKDIR /app

# Установка nginx
RUN apt-get update && \
    apt-get install -y --no-install-recommends nginx && \
    rm -rf /var/lib/apt/lists/*

# Отключаем дефолтный сайт nginx, чтобы он не перехватывал localhost
RUN rm -f /etc/nginx/sites-enabled/default

#Копируем nginx конфиг
COPY deploy/devops-project-313.conf /etc/nginx/conf.d/default.conf

COPY pyproject.toml /app/

RUN python3 -m pip install -e ".[dev]"

COPY /src ./src

#Копируем из фронтового образа скаченынй пакет с фронтовым приложением
COPY --from=front-build /node_modules/@hexlet/project-devops-deploy-crud-frontend/dist/. ./public/

EXPOSE 80

# инициализируем entrypoint.sh
COPY /deploy/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

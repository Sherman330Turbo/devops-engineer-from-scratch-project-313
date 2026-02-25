# Собираем фронтовый образ
FROM node:20-alpine AS front-build

WORKDIR /front

COPY package.json package-lock.json ./

RUN npm ci

FROM python:3.14.3-alpine3.23 AS runtime-build

WORKDIR /app

RUN apk add bash
RUN apk add --no-cache nginx

#Копируем nginx конфиг
COPY deploy/default.conf /etc/nginx/http.d/default.conf

COPY pyproject.toml /app/

RUN python3 -m pip install -e ".[dev]"

COPY /src ./src

#Копируем из фронтового образа скаченынй пакет с фронтовым приложением
COPY --from=front-build /front/node_modules/@hexlet/project-devops-deploy-crud-frontend/dist/. ./public/

EXPOSE 80

# инициализируем entrypoint.sh
COPY /deploy/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

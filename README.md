![Static Badge](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=yellow)
![Static Badge](https://img.shields.io/badge/mqtt-2.0.18-blue?logo=mqtt)
![Static Badge](https://img.shields.io/badge/docker-25.0.4-blue?logo=docker)
![Static Badge](https://img.shields.io/badge/redis-7.2.4-blue?logo=redis&logoColor=red)

## Сервис отправки

Представляет собой сервис сериализацией и отправкой данных на светодиодную матрицу.
Слушает сообщения из `REDIS` очереди, и при получении сообщения сериализует его и отправляет в `MQTT`

## Сборка

Для сборки приложения разработан [Dockerfile](https://github.com/awrura/sender/blob/main/docker/Dockerfile), запуск приложения осуществляется через него. **Важно**, перед запуском `docker`
контейнера необходимо создать и заполнить `.env` файл. Пример файла можно посмотреть в [.env.example](https://github.com/awrura/sender/blob/main/.env.example)

## Документация

Для просмотра документации можно использовать [asyncapi](https://studio.asyncapi.com/)
Конфигурацию можно взять в [asyncapi.yaml](https://github.com/awrura/sender/blob/main/asyncapi.yaml)

Жизненный цикл

![image](https://github.com/user-attachments/assets/a1c05980-337d-4368-9c60-51de169cc3df)


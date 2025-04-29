## Сервис отправки

Представляет собой сервис сериализацией и отправкой данных на светодиодную матрицу.
Слушает сообщения из `REDIS` очереди, и при получении сообщения сериализует его и отправляет в `MQTT`

## Сборка

Для сборки приложения разработан [Dockerfile](https://github.com/awrura/sender/blob/main/docker/Dockerfile), запуск приложения осуществляется через него. **Важно**, перед запуском `docker`
контейнера необходимо создать и заполнить `.env` файл. Пример файла можно посмотреть в [.env.example](https://github.com/awrura/sender/blob/main/.env.example)

## Документация

Для просмотра документации можно использовать [asyncapi](https://studio.asyncapi.com/)
Конфигурацию можно взять в [asyncapi.yaml](https://github.com/awrura/sender/blob/main/asyncapi.yaml)

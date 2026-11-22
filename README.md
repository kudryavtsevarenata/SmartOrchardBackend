# SmartOrchardBackend

Запуск (без миграций):
```
docker compose up -d --build
```

Запуск с миграциями:
```
docker compose --profile migrate up -d --build
```

Применить миграции:
```
docker compose run --rm migrate
```

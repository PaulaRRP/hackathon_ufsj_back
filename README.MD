Como buildar a imagem
----------------------

```
docker build --tag hacka_back-end .
```

Como rodar o serviço
----------------------

```
docker run -p 5000:5000 hacka_back-end
```

Como rodar o banco
-------------------

```
docker run -d -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=<sua-senha> --name mongodb mongo
```


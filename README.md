# mongo-oplog
## container start
```shell
docker-compose up -d
```
## replica set init 

```mongodb
rs.initiate(
  {
    _id : 'rs0',
    members: [
      { _id : 0, host : "mongo1:27017" },
      { _id : 1, host : "mongo2:27017" },
      { _id : 2, host : "mongo3:27017" }
    ]
  }
)
```

## mongo login

```mongodb
docker-compose exec mongo1 bash
mongo
```

## insert

```mongodb
db.products.insert( { _id: 10, item: "box", qty: 20 } )
```

## mongo oplog tailable cursor

```shell
docker-compose exec python bash
python main.py
```


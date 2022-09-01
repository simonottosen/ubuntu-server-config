# Server configuration

## To-do
- Automatic backup of the database 
-- docker exec -t cph_postgres_db pg_dumpall -c -U postgres | gzip > dump_$(date +"%Y-%m-%d").gz
- Environment variable also for the fetch-time container
- Expose model in seperate container

## Usage of the API

Get all
```
https://cphapi.simonottosen.dk/waitingtime
```

Get all times with a waiting time less that 4 minutes
```
https://cphapi.simonottosen.dk/waitingtime?t2waitingtime=lt.4
```

Select only a subset of the data
```
https://cphapi.simonottosen.dk/waitingtime?select=t2waitingtime,deliveryid
```


Get the current waiting time
```
https://cphapi.simonottosen.dk/waitingtime?select=t2waitingtime&order=id.desc&limit=1
```



## Deployment
Deploy the latest to the hook
```
simonottosen@servermat:~/mediaserver$ https POST webhook.simonottosen.dk/webhook/hooks/deploy
```


## When starting up a new server from bare metal
- Run git pull on the repostitory
- Set up .env (can be found in Dashlane)
- Run script.sh
- Test that the automatic deployment works

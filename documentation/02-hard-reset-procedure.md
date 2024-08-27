# Hard Reset of Steesh


## 1. Remove Docker Containers, Volumes, and Networks
This code removes **ALL** docker containers and their related data. 
```
sudo docker compose down -v
sudo docker stop $(sudo docker ps -aq);
sudo docker rm -v $(sudo docker ps -aq);
sudo docker rmi $(sudo docker images -q);
sudo docker volume rm $(sudo docker volume ls -q);
sudo docker network rm $(sudo docker network ls -q);
sudo docker system prune -a --volumes
```

## 2. Reset Local Code to Master
```
git reset --hard main
```
or
```
cd ..
sudo rm -rf it-security-steesh
```

## 3. Start Fresh
[Setup instructions](./01-first-setup.md)
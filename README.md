# Disciplina: Banco de Dados

Este repositorio contem exemplos de como criar um BD com o SGBD MariaDB.

## Instale o Docker e Docker Compose

```bash
# Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository    "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update -y
sudo apt-get install -y docker-ce docker-ce-cli containerd.io
sudo usermod -aG docker $USER
docker --version
``` 

## Atualize o SCRIPT de criação do BD

Atualize o seguinte script com as instruções apropriadas para criar seu BD ```maria/sql-scripts/CreateTable.sql```.

## Construa imgs docker e inicie o container do BD e da API

```bash
#MARIA DB
cd maria
sudo docker build -t maria .

export DB_PASSWORD=edu123
sudo docker run -e MYSQL_ROOT_PASSWORD=$DB_PASSWORD maria

# API
cd api
sudo docker build -t api-maria .

export MARIA_IP=$(sudo docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(sudo docker ps | grep maria | cut -f 1 -d ' '))
sudo docker run -e FLASK_APP=api-maria.py -e DB_HOST=$MARIA_IP -e DB_NAME=testeindexacao -e DB_USER=root -e DB_PASSWORD=edu123 api-maria:latest
```

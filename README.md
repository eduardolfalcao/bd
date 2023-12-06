# Disciplina: Banco de Dados

Este repositório contem um exemplo de como criar um BD com o SGBD MariaDB, e como criar uma API que serve de interface para o BD.

## Instale o Docker e Docker Compose

```bash
# Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository    "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update -y
sudo apt-get install -y docker-ce docker-ce-cli containerd.io
sudo usermod -aG docker $USER
docker --version

# Docker compose
sudo curl -L https://github.com/docker/compose/releases/download/1.26.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
# make it executable
sudo chmod +x /usr/local/bin/docker-compose
# check version
docker-compose --version
```

## Implantação do MariaDB

Primeiro sugiro que você olhe o Dockerfile que descreve a imagem que construiremos.
Depois, construa a imagem do container que usaremos para o MariaDB.

```bash
cd maria
vim Dockerfile
sudo docker build -t maria .
```

Agora execute a imagem do contêiner que você construiu:
```bash
export DB_PASSWORD=senha123
sudo docker run -e MYSQL_ROOT_PASSWORD=$DB_PASSWORD maria
```

Neste ponto, temos um container MariaDB levantado e escutando por requisições.

## Python Flask API to interact with Maria

Crie a imagem do container com a API Flask.
Primeiro sugiro que você compreenda o conteúdo dos arquivos no diretório api: api-maria.py, requirements.txt, e Dockerfile.
Uma vez que você tenha compreendido a ideia básica de funcionamento da API e do Dockerfile, vamos constuir a imagem do container.

```bash
cd api
sudo docker build -t api-maria .
```

Descubra ip do BD:
```bash
export MARIA_IP=$(sudo docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(sudo docker ps | grep maria | cut -f 1 -d ' '))
```

Por fim, executa a API Flask:
```bash
cd api
sudo docker run -e FLASK_APP=api-maria.py -e DB_HOST=$MARIA_IP -e DB_NAME=iot_sensor -e DB_USER=root -e DB_PASSWORD=senha123 api-maria:latest
```

## Interagindo com o MariaDB através da API

### Add people count
Adiciona uma quantidade de pessoas detectadas por determinado coletor em determinado momento.

* **URL**: `/add_people_count`
* **Method:** `POST`
* **Parameters**:
    1. `value` - people count (int)
    2. `collector_id` - collector iot device identification (string)
    3. `timestamp` - timestamp of detection (int)

* **Exemplo de requisição com CURL**:
```bash
curl http://172.17.0.3:8080/add_people_count \
     --request POST --header "Content-Type: application/json" \
     --data '{
              "value": 23, 
              "collector_id": "iot_dev_id_1", 
              "timestamp": 342342
             }'
```

### Add people recognized
Adiciona pessoas reconhecidas por determinado sensor em determinado momento.

* **URL**: `/add_people_recognized`
* **Method:** `POST`
* **Parameters**:
    1. `value` - list of people's name recognized (list of string)
    2. `collector_id` - collector iot device identification (string)
    3. `timestamp` - timestamp of detection (int)

* **Exemplo de requisição com CURL**:
```bash
curl http://172.17.0.3:8080/add_people_recognized \
     --request POST --header "Content-Type: application/json" \
     e-data '{
     l        "value": ["andrey", "eduardo", "fabio"], 
* **Request example with CURL**:
              "collector_id": "iot_dev_id_2", 
              "timestamp": 3423
             }'
```

### Get people recognized
Obter todas as pessoas reconhecidas.

* **URL**: `/get_people_recognized`
* **Method:** `GET`
* **Parameters**: none

* **Exemplo de requisição com CURL**:
```basl
curl http://172.17.0.3:8080/get_people_recognized --request GET 
```

### Get people count
Obter quantidade de pessoas detectadas.

* **URL**: `/get_people_count`
* **Method:** `GET`
* **Parameters**: none

* **Exemplo de requisição com CURL**:
```bash
curl http://172.17.0.3:8080/get_people_count --request GET 
```

### Get people count per collector id
Obter quantidade de pessoas detectadas por um coletor específico (pelo seu id).

* **URL**: `/get_people_count_per_collector`
* **Method:** `GET`
* **Parameters**:
    1. `collector_id` - collector iot device identification (string)

* **Exemplo de requisição com CURL**:
```bash
curl http://172.17.0.3:8080/get_people_count_per_collector --request GET \
     --header "Content-Type: application/json" \
     --data '{
              "collector_id": "iot_dev_id_1"
             }'
```

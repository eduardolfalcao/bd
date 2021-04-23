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

# Docker compose
sudo curl -L https://github.com/docker/compose/releases/download/1.26.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
# make it executable
sudo chmod +x /usr/local/bin/docker-compose
# check version
docker-compose --version
``` 

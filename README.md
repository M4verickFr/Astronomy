# 🚀🌌 PROJ 932 - Astronomy

[![forthebadge](http://forthebadge.com/images/badges/built-with-love.svg)](http://forthebadge.com)  [![forthebadge](http://forthebadge.com/images/badges/powered-by-electricity.svg)](http://forthebadge.com)

## 🔍 Overview

Spativis is a high quality space viewer designed for astronomy professionals and enlightened amateurs. It offers an immersive and interactive experience to explore the sky and discover the wonders of the universe.

With its advanced visualization features, you can see sky objects in their true position in space and understand how they relate to each other. The data displayed in Spativis has been pre-processed for better readability and easy understanding, such as supernovas highlighted for increased visibility.

## 🔥  Features
## 👀 Quick overview of our project 

TODO: Des screens du projet 

## ⚙️ Project structure

```
.
├── compose.yaml
├── flask
│   ├── Dockerfile
│   ├── requirements.txt
│   └── server.py
└── nginx
    └── nginx.conf
```

## 🛠️ **How to use** 

1️⃣ **Cloner le Git**

2️⃣ **Assurer-vous que docker est démarre**

3️⃣ **Ensuite, exécutez la commande `docker compose up -d` dans le dossier du projet**

```
$ docker compose up -d
Creating network "nginx-flask-mongo_default" with the default driver
Pulling mongo (mongo:)...
latest: Pulling from library/mongo
423ae2b273f4: Pull complete
...
...
Status: Downloaded newer image for nginx:latest
Creating nginx-flask-mongo_mongo_1 ... done
Creating nginx-flask-mongo_backend_1 ... done
Creating nginx-flask-mongo_web_1     ... done
```

4️⃣ **Expected result**

Listing containers must show three containers running and the port mapping as below:
```
$ docker ps
CONTAINER ID        IMAGE                        COMMAND                  CREATED             STATUS              PORTS                  NAMES
a0f4ebe686ff        nginx                       "/bin/bash -c 'envsu…"   About a minute ago   Up About a minute   0.0.0.0:80->80/tcp     nginx-flask-mongo_web_1
dba87a080821        nginx-flask-mongo_backend   "./server.py"            About a minute ago   Up About a minute                          nginx-flask-mongo_backend_1
d7eea5481c77        mongo                       "docker-entrypoint.s…"   About a minute ago   Up About a minute   27017/tcp              nginx-flask-mongo_mongo_1
```

After the application starts, navigate to `http://localhost:81` in your web browser

5️⃣ **Stop and remove the containers**
```
$ docker compose down
```

## 🏗️ Developed with

* [Python](https://www.python.org/)
* [Docker](https://www.mongodb.com/)
* [MongoDB](https://www.mongodb.com/)
* [Flask](https://www.mongodb.com/)
* [AladinLite](https://www.mongodb.com/)
* [Boostrap](https://nodejs.org/en/)
* [jQuery](https://nodejs.org/en/)

## 💪 Authors of this project

* **PERROLLAZ Maverick** _alias_ [@M4verickFr](https://github.com/M4verickFr)
* **KOEBERLE Celien** _alias_ [@caullird](https://github.com/koeberlc)
* **THESE Doriane** _alias_ [@caullird](https://github.com/thezedoriane)
* **YAO Xin** _alias_ [@caullird](https://github.com/Xin-YAO1)





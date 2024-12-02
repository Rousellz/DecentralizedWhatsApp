#!/bin/bash

# Desactivar modo detallado
set +o verbose

# Detener y eliminar todos los contenedores que se puedan estar ejecutando
docker stop $(docker ps -aq) 2>/dev/null
docker rm $(docker ps -aq) 2>/dev/null

# Eliminar las redes de cliente y servidor si existen
docker network rm clients_network servers_network 2>/dev/null

# Eliminar las imágenes de cliente, servidor y router si existen
# docker rmi router image_client image_server 2>/dev/null

# Eliminar volúmenes antiguos
docker volume prune -f

# Verificar la existencia de la red de clientes y crearla si no existe
docker network inspect clients_network >/dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "Network clients_network exists."
else
    docker network create clients_network --subnet 10.0.20.0/24
    echo "Network clients_network created."
fi

# Verificar la existencia de la red de servidores y crearla si no existe
docker network inspect servers_network >/dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "Network servers_network exists."
else
    docker network create servers_network --subnet 10.0.21.0/24
    echo "Network servers_network created."
fi

# Verificar la existencia de la imagen del router y construirla si no existe
docker image inspect image_router >/dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "Image image_router exists."
else
    docker build -t image_router -f router/Dockerfile .
    echo "Image image_router created."
fi

# Verificar la existencia del contenedor del router y eliminarlo si existe
docker container inspect container_router >/dev/null 2>&1
if [ $? -eq 0 ]; then
    docker container stop container_router
    docker container rm container_router
    echo "Container container_router removed."    
fi

# Ejecutar el contenedor del router
docker run -d --rm --name container_router image_router
echo "Container router executed."

# Conectar el router a las redes de clientes y servidores
docker network connect --ip 10.0.20.254 clients_network container_router
docker network connect --ip 10.0.21.254 servers_network container_router
echo "Container container_router connected to clients_network and servers_network networks."
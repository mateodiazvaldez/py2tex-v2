#!/bin/bash

DOCKER_IMAGE="py2tex-automatizado"

# 1. Construir la imagen (solo se hace una vez o después de cambios en el Dockerfile)
echo "Construyendo la imagen Docker..."
docker build -t $DOCKER_IMAGE .

# 2. Ejecutar el contenedor, montando los directorios locales
echo "Ejecutando el procesador..."
docker run --rm \
    -v "$(pwd)/src:/app/src" \
    -v "$(pwd)/output:/app/output" \
    $DOCKER_IMAGE \
    /bin/bash /app/convert.sh # Llama al script de conversión dentro del contenedor

echo "Proceso completado. Revisa la carpeta 'output/txt' para tus archivos .tex."
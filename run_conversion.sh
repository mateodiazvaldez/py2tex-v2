#!/bin/bash

DOCKER_IMAGE="py2tex-automatizado"

# 1. Construir la imagen
echo "Construyendo la imagen Docker..."
docker build -t $DOCKER_IMAGE .

# 2. Ejecutar el contenedor
echo "Ejecutando el procesador..."
docker run --rm \
    -v "$(pwd)/src:/app/src" \
    -v "$(pwd)/output:/app/output" \
    $DOCKER_IMAGE \
    /usr/local/bin/convert_exec.sh # <- ¡Esta es la línea corregida!

echo "Proceso completado. Revisa la carpeta 'output/txt' para tus archivos .tex."
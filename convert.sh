#!/bin/bash
# Script que se ejecuta DENTRO de Docker

SRC_DIR="/app/src"
OUTPUT_DIR="/app/output/txt"

mkdir -p "$OUTPUT_DIR"

echo "Iniciando conversión de archivos .py a .tex..."

# Itera sobre todos los archivos Python en la carpeta montada
for file_path in $SRC_DIR/*.py; do
    if [ -f "$file_path" ]; then
        filename=$(basename -- "$file_path")
        rootname="${filename%.*}"
        output_file="$OUTPUT_DIR/$rootname.tex"
        
        echo "  -> Procesando $filename..."

        # 1. Escribir el inicio del entorno contenedor (\begin{algorithm})
        # [H] fuerza la colocación aquí.
        echo '\begin{algorithm}[H]' > "$output_file"
        echo "\caption{Pseudocódigo del algoritmo: \texttt{$rootname}}" >> "$output_file"
        echo '\label{alg:'"$rootname"'}' >> "$output_file"
        echo '\begin{algorithmic}[1]' >> "$output_file"

        # 2. Ejecutar py2tex.py y AÑADIR su contenido
        python3 /usr/local/bin/py2tex_exec.py "$file_path" >> "$output_file"

        # 3. Escribir el cierre de los entornos
        echo '\end{algorithmic}' >> "$output_file"
        echo '\end{algorithm}' >> "$output_file"
    fi
done

echo "Conversión finalizada. Archivos .tex listos en output/txt/."
# Usa una imagen base de Linux (Debian)
FROM debian:bookworm-slim

# Instalar dependencias esenciales (Tex Live, Python, paquetes de LaTeX)
RUN apt update && \
    apt install -y \
        python3 \
        texlive \
        texlive-latex-extra \
        texlive-science \
        texlive-lang-spanish \
        --no-install-recommends && \
    apt clean

# Crear el directorio para el paquete .sty y copiar los archivos
RUN mkdir -p /usr/local/share/texmf/tex/latex/py2tex
# Copia el estilo py2tex.sty
COPY py2tex_files/py2tex.sty /usr/local/share/texmf/tex/latex/py2tex/
# Copia el ejecutable python
COPY py2tex_files/py2tex.py /usr/local/bin/py2tex_exec.py

# Actualizar la base de datos de LaTeX para que encuentre el .sty
RUN texhash

# Copiar el script de conversión
COPY convert.sh /usr/local/bin/convert_exec.sh
# Dar permisos de ejecución
RUN chmod +x /usr/local/bin/convert_exec.sh
# Corregir el formato de saltos de línea (CRLF a LF) de forma permanente dentro de Docker
RUN sed -i 's/\r$//' /usr/local/bin/convert_exec.sh

WORKDIR /app
ENTRYPOINT ["/bin/bash"]
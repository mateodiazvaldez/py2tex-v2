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

# Definir el directorio de trabajo
WORKDIR /app

# El punto de entrada será Bash, para poder ejecutar el script de conversión
ENTRYPOINT ["/bin/bash"]
@echo off
SET DOCKER_IMAGE=py2tex-automatizado
SET CURRENT_DIR=%~dp0

echo.
echo ======================================================
echo 1. Construyendo la imagen Docker
echo ======================================================
docker build -t %DOCKER_IMAGE% .

IF ERRORLEVEL 1 (
    echo.
    echo ERROR: La construccion de la imagen fallo.
    pause
    goto :eof
)

echo.
echo ======================================================
echo 2. Ejecutando la conversion y montando directorios
echo ======================================================

REM El comando monta los directorios y luego ejecuta una cadena de comandos:
REM 1. sed -i 's/\r$//' /app/convert.sh: Limpia los saltos de linea (CRLF a LF).
REM 2. &&: Solo si la limpieza fue exitosa.
REM 3. /app/convert.sh: Ejecuta el script de conversion.

docker run --rm ^
    -v "%CURRENT_DIR%src:/app/src" ^
    -v "%CURRENT_DIR%output:/app/output" ^
    -v "%CURRENT_DIR%convert.sh:/app/convert.sh" ^
    %DOCKER_IMAGE% /bin/bash -c "sed -i 's/\r$//' /app/convert.sh && /app/convert.sh"

echo.
echo ======================================================
echo Proceso completado. Revisa la carpeta 'output/txt'.
echo ======================================================
pause
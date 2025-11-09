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

REM El comando usa la tubería para limpiar los saltos de línea y ejecutar el script.
docker run --rm --entrypoint /bin/bash -v "%CURRENT_DIR%src:/app/src" -v "%CURRENT_DIR%output:/app/output" -v "%CURRENT_DIR%convert.sh:/app/convert.sh" %DOCKER_IMAGE% -c "cat /app/convert.sh | tr -d '\r' | bash"

echo.
echo ======================================================
echo Proceso completado. Revisa la carpeta 'output/txt'.
echo ======================================================
pause
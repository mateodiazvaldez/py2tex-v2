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

REM Ejecutar el script pre-copiado y formateado con el comando simple.
docker run --rm ^
    -v "%CURRENT_DIR%src:/app/src" ^
    -v "%CURRENT_DIR%output:/app/output" ^
    %DOCKER_IMAGE% /usr/local/bin/convert_exec.sh

echo.
echo ======================================================
echo Proceso completado. Revisa la carpeta 'output/txt'.
echo ======================================================
pause
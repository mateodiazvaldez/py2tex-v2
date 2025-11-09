# Py2TeX v2: Automatizado con Docker

Este proyecto convierte código fuente de Python simple en pseudocódigo LaTeX listo para importar. Es una versión mejorada del repositorio original `cairomassimo/py2tex`, modernizada para funcionar en cualquier sistema operativo (Windows, macOS, Linux) gracias a Docker.

## Características

* **Multiplataforma:** Se ejecuta en un contenedor de Docker. No necesitas instalar Python, TeX Live ni ninguna dependencia en tu máquina.
* **Salida Lista para Usar:** Genera archivos `.tex` que son "importables" directamente. El script los envuelve automáticamente en los entornos `\begin{algorithm}` y `\begin{algorithmic}`.

---

## 🚀 Cómo Usarlo

El proceso está 100% automatizado.

### 1. Prepara tus archivos
Coloca todos los archivos `.py` que quieras convertir dentro de la carpeta `/src`.
* Por defecto, este proyecto incluye `example.py` para que puedas probarlo de inmediato.

### 2. Ejecuta el Script de Conversión
Solo necesitas tener Docker Desktop instalado y ejecutándose.

* **En Windows:**
    Haz doble clic en `run_conversion.cmd`.

* **En macOS o Linux:**
    Ejecuta `./run_conversion.sh` en tu terminal. (Asegúrate de darle permisos primero con `chmod +x run_conversion.sh`).

### 3. Revisa la Salida
El script construirá la imagen de Docker (solo la primera vez) y luego la ejecutará.

Encontrarás tus archivos `.tex` listos en la carpeta `/output/txt`. Por ejemplo, `example.py` se convertirá en `output/txt/example.tex`.

---

## 📥 Cómo Importar el Pseudocódigo a LaTeX

Tu archivo `.tex` principal (ej. `tesis.tex`, `informe.tex`) debe estar configurado para entender los comandos del archivo generado.

### Paso 1: Copia el Archivo de Estilo
Copia el archivo `py2tex_files/py2tex.sty` a la misma carpeta donde está tu archivo `.tex` principal.

### Paso 2: Carga los Paquetes en tu Preámbulo
En tu archivo `.tex` principal, asegúrate de que tu preámbulo (la parte antes de `\begin{document}`) contenga los siguientes paquetes:

\documentclass{article}

% --- PAQUETES REQUERIDOS ---
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}

% Paquetes para algoritmos
\usepackage{algorithm}     % Para el entorno \begin{algorithm}
\usepackage{algorithmicx}  % Requerido por algpseudocode
\usepackage{algpseudocode} % Requerido por py2tex.sty

% --- TU PAQUETE DE ESTILOS ---
\usepackage{py2tex}        % Carga el archivo py2tex.sty
% -------------------------

\begin{document}

### Paso 3: Importa tu Algoritmo
En el cuerpo de tu documento, usa el comando \input{} para incluir el archivo .tex generado:

\documentclass{article}
% ... (todos los paquetes del Paso 2) ...
\begin{document}

\section{Análisis de Algoritmos}
A continuación, se presenta el pseudocódigo del algoritmo de ejemplo,
generado automáticamente desde la fuente de Python.

% Aquí importas el archivo (ajusta la ruta si es necesario)
\input{output/txt/example.tex}

El análisis continúa después del algoritmo...

\end{document}
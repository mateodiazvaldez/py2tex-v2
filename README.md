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

```latex
\documentclass{article}

% --- PAQUETES REQUERIDOS ---
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[spanish]{babel} % Recomendado para LaTeX en español

% Paquetes para algoritmos
\usepackage{algorithm}     % Para el entorno \begin{algorithm}
\usepackage{algorithmicx}  % Requerido por algpseudocode
\usepackage{algpseudocode} % Requerido por py2tex.sty

% --- TU PAQUETE DE ESTILOS ---
\usepackage{py2tex}        % Carga el archivo py2tex.sty
% -------------------------

\begin{document}
````

### Paso 3: Importa tu Algoritmo

En el cuerpo de tu documento, usa el comando `\input{}` para incluir el archivo `.tex` generado:

```latex
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
```

¡Eso es todo\! Al compilar tu `.tex` principal, LaTeX encontrará el archivo `example.tex`, leerá su contenido y lo renderizará como un algoritmo con formato.

-----

## 🎨 Personalización Avanzada

Puedes personalizar la apariencia y el idioma del pseudocódigo generado.

### 1\. Cambiar el Idioma a Español

Las palabras clave del pseudocódigo (como `function`, `if`, `while`, etc.) se definen en el archivo de estilo de LaTeX.

**Archivo a modificar:** `py2tex_files/py2tex.sty`

**A. Palabras Clave (Línea 50 aprox.):**
Busca este bloque de código:

```latex
\algrenewcommand\algorithmicprocedure{{\textbs{procedure}}}
\algrenewcommand\algorithmicfunction{{\textbs{function}}}
\algrenewcommand\algorithmicif{{\textbs{if}}}
\algrenewcommand\algorithmicthen{{\textbs{then}}}
\algrenewcommand\algorithmicelse{{\textbs{else}}}
\algrenewcommand\algorithmicwhile{{\textbs{while}}}
% ... etc.
```

Y reemplaza las palabras en inglés por las de tu preferencia:

```latex
\algrenewcommand\algorithmicprocedure{{\textbs{procedimiento}}}
\algrenewcommand\algorithmicfunction{{\textbs{función}}}
\algrenewcommand\algorithmicif{{\textbs{si}}}
\algrenewcommand\algorithmicthen{{\textbs{entonces}}}
\algrenewcommand\algorithmicelse{{\textbs{sino}}}
\algrenewcommand\algorithmicwhile{{\textbs{mientras}}}
% ... etc.
```

**B. Traducir "print" (Línea 80 aprox.):**
Para cambiar el comando `print` (que por defecto es "output"), busca:

```latex
\newcommand{\PyCall}[2]{
	\ifnum\pdfstrcmp{#1}{print}=0
  	\textbs{output~} { \tt#2} 
	\else
% ...
```

Y cámbialo por la palabra en español que prefieras (ej. `mostrar`):

```latex
% ...
  	\textbs{mostrar~} { \tt#2} 
% ...
```

Después de guardar estos cambios, solo vuelve a ejecutar `run_conversion.cmd` o `run_conversion.sh`. El `docker build` detectará los cambios.

### 2\. Quitar el "Algorithm 1" del Título

Para que el algoritmo no se numere y solo muestre tu `\caption`, puedes usar el entorno `algorithm*` (con asterisco).

**Archivo a modificar:** `convert.sh`

  * **Línea 19 (aprox.):** Cambia `\begin{algorithm}[H]` por `\begin{algorithm*}[H]`.
  * **Línea 26 (aprox.):** Cambia `\end{algorithm}` por `\end{algorithm*}`.

<!-- end list -->

```
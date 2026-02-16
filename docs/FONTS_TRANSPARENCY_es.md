# Proceso de obtención de fuentes libres y generación de TTF estáticos

## 1. Objetivo

El objetivo es sustituir un conjunto de fuentes `.ttf` no redistribuibles (p. ej. Arial, Verdana, Impact, Consolas) por fuentes **libres** que puedan incluirse legalmente en un proyecto con licencia MIT, manteniendo en lo posible el comportamiento visual y de métricas (“layout”) del proyecto.

El resultado final que se ofrece para su uso y redistribución es un **directorio plano** con fuentes `.ttf` estáticas (Regular, Bold, Italic, BoldItalic) que puedan cargarse en Pygame con:

```python
pygame.font.Font("fonts_runtime/Inter-Regular.ttf", 18)
```

Además, se conservan los ficheros de licencia correspondientes.

---

## 2. Fuente de origen y justificación

### 2.1. Por qué no se usa “descarga directa” desde fonts.google.com

Se intentó un método de descarga automatizada desde Google Fonts usando el endpoint de descarga de la web. En la práctica, este endpoint puede devolver HTML u otras respuestas que no son un ZIP de fuentes válido en un contexto automatizado, lo que puede dejar directorios vacíos o incompletos.

Por transparencia y reproducibilidad, se adoptó un origen más estable.

### 2.2. Origen definitivo: repositorio oficial `google/fonts`

La descarga se hace desde el repositorio oficial:

- **Repositorio**: `google/fonts` (GitHub)

Este repositorio contiene:
- archivos `.ttf` (incluyendo variables y/o estáticos según familia),
- texto de licencia por familia (por ejemplo `OFL.txt`, `LICENSE.txt`),
- metadatos (`METADATA.pb`) y descripción (`DESCRIPTION.en_us.html`).

La presencia del fichero de licencia por familia y la estructura organizada del repositorio facilitan un uso transparente y auditable.

---

## 3. Descarga inicial de familias tipográficas

### 3.1. Selección de familias

Se seleccionaron fuentes libres con el objetivo de cubrir sustitutos razonables para fuentes no redistribuibles habituales y, adicionalmente, aportar algunas fuentes “artísticas”.

Ejemplos de familias utilizadas:
- Anton (sustituto práctico de Impact)
- Arimo (sustituto práctico de Arial)
- Inter (sustituto moderno para UI, alternativa práctica para Verdana)
- IBM Plex Mono (sustituto de Consolas)
- Yrsa (serif libre)
- Varias fuentes display (Bebas Neue, Lobster, Monoton, Pacifico, etc.)

### 3.2. Qué se descargó realmente

Para cada familia, el repositorio suele contener:
- uno o más `.ttf` (a veces variables con ejes, a veces estáticos),
- `OFL.txt` o `LICENSE.txt`,
- y ficheros informativos opcionales (`METADATA.pb`, `DESCRIPTION.en_us.html`).

Esta descarga se organizó en un directorio de trabajo con estructura por familia, por ejemplo:

```
fonts/
  Inter/
    Inter[opsz,wght].ttf
    Inter-Italic[opsz,wght].ttf
    OFL.txt
    METADATA.pb
    DESCRIPTION.en_us.html
  Arimo/
    Arimo[wght].ttf
    Arimo-Italic[wght].ttf
    LICENSE.txt
    ...
  ...
```

---

## 4. Consideración clave: fuentes variables vs. estáticas

### 4.1. Qué significa `[wght]` o `[opsz,wght]` en el nombre

Cuando el nombre del archivo incluye corchetes, por ejemplo:

- `Arimo[wght].ttf`
- `Inter[opsz,wght].ttf`

significa que es una **fuente variable** (variable font).

Los ejes frecuentes son:
- `wght`: peso (regular/bold/etc.)
- `opsz`: tamaño óptico (ajustes tipográficos según tamaño)

### 4.2. Por qué se generan fuentes estáticas

En Pygame, el uso típico es seleccionar un archivo `.ttf` concreto:

```python
pygame.font.Font("fonts_runtime/Inter-Bold.ttf", 18)
```

Aunque Pygame puede cargar una fuente variable como un `.ttf` normal, no es práctico depender de mecanismos internos para seleccionar ejes tipográficos (peso, tamaño óptico). Para controlar el resultado y facilitar sustituciones de fuentes como “Arial Bold” o “Verdana Bold Italic”, se decidió generar **instancias estáticas**.

---

## 5. Generación de los `.ttf` finales para distribución

### 5.1. Estructura final entregada para uso en el proyecto

Se generó un directorio de runtime plano:

```
fonts_runtime/
  Inter-Regular.ttf
  Inter-Bold.ttf
  Inter-Italic.ttf
  Inter-BoldItalic.ttf
  Arimo-Regular.ttf
  Arimo-Bold.ttf
  Arimo-Italic.ttf
  Arimo-BoldItalic.ttf
  IBMPlexMono-Regular.ttf
  IBMPlexMono-Bold.ttf
  IBMPlexMono-Italic.ttf
  IBMPlexMono-BoldItalic.ttf
  Yrsa-Regular.ttf
  ...
  licenses/
    Inter/OFL.txt
    Arimo/LICENSE.txt
    ...
  fonts_runtime.json
  font_replacements.json
```

### 5.2. Criterio de generación

Se aplicaron estas reglas:

#### Familias con fuentes estáticas ya disponibles
Si en la familia existen archivos como:
- `Family-Regular.ttf`
- `Family-Bold.ttf`
- `Family-Italic.ttf`
- `Family-BoldItalic.ttf`

se copiaron directamente los `.ttf` a `fonts_runtime/` renombrándolos a un formato uniforme:

- `Family-Regular.ttf`
- `Family-Bold.ttf`
- etc.

#### Familias con fuentes variables
Si la familia trae fuentes variables, se generan 4 instancias estáticas:

- Regular  → `wght=400`
- Bold     → `wght=700`
- Italic   → (archivo italic variable si existe) con `wght=400`
- BoldItalic → (archivo italic variable si existe) con `wght=700`

Para `opsz` se fijó un valor consistente:

- `opsz=14`

Esto reduce variaciones inesperadas y hace más reproducible el resultado.

### 5.3. Herramienta utilizada para instanciación

Para convertir fuentes variables a instancias estáticas se utilizó:

- **fontTools** (paquete Python)

Instalación típica:

```bash
pip install fonttools
```

---

## 6. Licencias y trazabilidad

### 6.1. Conservación de licencias

Para cada familia se copiaron los ficheros de licencia al directorio:

```
fonts_runtime/licenses/<Family>/
```

Sin modificar el contenido de los textos de licencia.

### 6.2. Inventario generado

Se generó un inventario `fonts_runtime/fonts_runtime.json` que contiene, por cada `.ttf` final:

- familia
- estilo
- nombre del fichero final
- origen (si fue copia directa o instancia de variable)
- fichero fuente original dentro de la familia
- ejes utilizados (wght, opsz si aplica)
- licencias asociadas

Este fichero permite auditar exactamente:
- de qué archivo original proviene cada `.ttf`,
- y bajo qué licencia se distribuye.

### 6.3. Mapeo de sustitución

Se generó un fichero `fonts_runtime/font_replacements.json` con el mapeo desde los nombres antiguos (no redistribuibles) hacia los nuevos `.ttf` libres.

Ejemplos típicos:
- `Impact.ttf` → `Anton-Regular.ttf`
- `ariali.ttf` → `Arimo-Italic.ttf`
- `arialbd.ttf` → `Arimo-Bold.ttf`
- `Verdana.ttf` → `Inter-Regular.ttf`
- `Verdana_Bold_Italic.ttf` → `Inter-BoldItalic.ttf`
- `Consolas.ttf` → `IBMPlexMono-Regular.ttf`
- `Yrsa-Medium.ttf` → `Yrsa-Regular.ttf`

Esto permite sustituir en el proyecto las referencias antiguas por rutas a `fonts_runtime/*.ttf`.

---

## 7. Advertencias y casos especiales

Algunas familias no ofrecen 4 estilos reales. Ejemplos típicos:
- Familias display que solo tienen Regular (Anton, Bebas Neue, etc.)
- Algunas fuentes artísticas no tienen italic real.
- Algunas familias pueden ofrecer solo Bold.

En estos casos se mantiene la transparencia:
- el inventario registra qué estilos existen realmente,
- y se evita crear “falsos itálicos” (oblique artificial) salvo que se decida explícitamente lo contrario.

---

## 8. Verificación recomendada

Para validar que el runtime final es utilizable:

1) Comprobar que existen `.ttf` en `fonts_runtime/`.
2) Cargar algunos en Pygame (ejemplo):
   ```python
   pygame.font.Font("fonts_runtime/Inter-Regular.ttf", 18)
   ```
3) Usar `FontViewer.py` para verificar visualmente y revisar el JSON completo de cada fuente.

---

## 9. Resultado

El resultado es un conjunto de `.ttf` libres y redistribuibles, con:
- nombres consistentes,
- directorio plano compatible con el uso típico en Pygame,
- licencias conservadas por familia,
- e inventario + mapeo que facilitan auditoría y sustitución en el proyecto.

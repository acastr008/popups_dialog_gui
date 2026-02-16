# Guía de equivalencias de fuentes y creación de estilos (styles/*.json)

Este documento explica, paso a paso, cómo sustituir fuentes no redistribuibles por fuentes de libre uso, como procedimos a ello en nuestro caso y en general cómo definir nuevos estilos dentro del fichero JSON de estilos.

La guía está pensada para trabajar con el JSON de estilos existente `assets/styles/popup_gui.json`)
donde aparecen referencias a fuentes que no son libres, tales como `Impact.ttf`, `ariali.ttf`, `Verdana.ttf`, etc. 

---

## 1. Contexto y objetivo

En el JSON de estilos actual existen estilos como `playful_childlike` y `formal`, con campos de fuente similares a:

- `Tit_FontType` (título)
- `Krn_FontType` (texto “kernel” / cuerpo)
- `Lbt_FontType` (labels/botones)
- En el estilo “formal”, además:
  - `hlp_Font`, `hlp_FontBold`, `hlp_CodeFont`

El objetivo es que todos esos campos apunten a fuentes libres incluidas en el repositorio del proyecto
(para que el proyecto sea redistribuible y reproducible).

---

## 2. Qué se considera “equivalencia” de fuente

Una “equivalencia” no significa que la fuente sea idéntica. Significa que:

1. Es **libre y redistribuible** (con licencia incluida).
2. Cumple un rol similar (display / sans / mono / serif).
3. Mantiene en lo posible el **layout** (anchos/altos de texto y saltos de línea) dentro del proyecto.

En esta guía se asume que ya disponemos de un directorio plano de runtime con las fuentes finales, por ejemplo:

```
fonts/
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
  Yrsa-Bold.ttf
  Yrsa-Italic.ttf
  Yrsa-BoldItalic.ttf
  Anton-Regular.ttf
  ...
  licenses/...
```

Si en tu proyecto usas otro directorio (por ejemplo `assets/fonts/`), simplemente copia ahí los `.ttf` o ajusta
tu “asset locator” para buscar en `fonts_runtime/`.

---

## 3. Tabla de sustitución recomendada (casos actuales del JSON)

Estas son las sustituciones directas recomendadas para los nombres que aparecen en el JSON de estilos actual:

| Fuente antigua (no redistribuible o no deseada) | Sustituto libre recomendado                              | Motivo / comentario                                              |
| ----------------------------------------------- | -------------------------------------------------------- | ---------------------------------------------------------------- |
| `Impact.ttf`                                    | `Anton-Regular.ttf`                                      | Display fuerte para títulos. Sustituto práctico de Impact.       |
| `ariali.ttf` (Arial Italic)                     | `Arimo-Italic.ttf`                                       | Sans “Arial-like”, buena compatibilidad de métricas.             |
| `arialbd.ttf` (Arial Bold)                      | `Arimo-Bold.ttf`                                         | Bold real (no “fake bold”).                                      |
| `Verdana.ttf`                                   | `Inter-Regular.ttf`                                      | Sans de UI moderna. Alternativa estable en pantalla.             |
| `Verdana_Bold_Italic.ttf`                       | `Inter-BoldItalic.ttf`                                   | Mantiene el rol “título”/énfasis en estilo formal.               |
| `Consolas.ttf`                                  | `IBMPlexMono-Regular.ttf`                                | Monoespaciada moderna y redistribuible.                          |
| `Yrsa-Medium.ttf`                               | `Yrsa-Regular.ttf` *(o `Yrsa-Medium.ttf` si la generas)* | Serif libre. Si necesitas “Medium” exacto, genera esa instancia. |

Notas:

- Si tu código solo usa `pygame.font.Font(path, size)` y no aplica estilos a posteriori,
  es preferible usar ficheros estáticos “reales” (`*-Bold.ttf`, `*-Italic.ttf`, etc.).
- Evita depender de “fake bold / fake italic” (p. ej. `set_bold(True)`) si buscas estabilidad de layout.

---

## 4. Cambios realizados en popup_gui.json para migrar fuentes libres

| Estilo.atributo                | Fuente previa           | Nueva fuente libre      |
|:------------------------------:|:-----------------------:|:-----------------------:|
| playful_childlike.Tit_FontType | Impact.ttf              | Anton-Regular.ttf       |
| playful_childlike.Krn_FontType | ariali.ttf              | Arimo-Italic.ttf        |
| playful_childlike.Lbt_FontType | arialbd.ttf             | Arimo-Bold.ttf          |
| formal.Tit_FontType            | Verdana_Bold_Italic.ttf | Inter-BoldItalic.ttf    |
| formal.Krn_FontType            | Yrsa-Medium.ttf         | Yrsa-Regular.ttf        |
| formal.Lbt_FontType            | Verdana.ttf             | Inter-Regular.ttf       |
| formal.hlp_Font                | Yrsa-Medium.ttf         | Yrsa-Regular.ttf        |
| formal.hlp_FontBold            | Verdana_Bold_Italic.ttf | Inter-BoldItalic.ttf    |
| formal.hlp_CodeFont            | Consolas.ttf            | IBMPlexMono-Regular.ttf |

---

## 5. Cómo añadir tu propio estilo al JSON

### 5.1. Paso 1: clonar un estilo existente

La forma más segura es copiar un bloque completo (por ejemplo `formal`) y renombrar la clave del estilo:

```json
"my_style": {
  "...": "...",
  "Tit_FontType": "Inter-BoldItalic.ttf",
  "Krn_FontType": "Yrsa-Regular.ttf",
  "Lbt_FontType": "Inter-Regular.ttf"
}
```

### 5.2. Paso 2: decidir roles de fuente

Para mantener consistencia, decide qué familia usar para cada rol:

- **Títulos (Tit_)**: display o sans con peso alto (p. ej. `Inter-Bold.ttf`, `Inter-BoldItalic.ttf`, `Anton-Regular.ttf`).
- **Texto principal (Krn_)**: serif o sans legible (p. ej. `Yrsa-Regular.ttf`, `Inter-Regular.ttf`, `Arimo-Regular.ttf`).
- **Botones/labels (Lbt_)**: sans claro y consistente (p. ej. `Inter-Regular.ttf`, `Arimo-Regular.ttf`).
- **Código (hlp_CodeFont)**: monoespaciada (p. ej. `IBMPlexMono-Regular.ttf`).

### 5.3. Paso 3: validar tamaños y layout

Recomendación práctica:

1. Elige tamaños (`*_FontSize`) manteniendo los actuales.
2. Renderiza una pantalla “representativa” del UI.
3. Ajusta **solo** si observas:
   - textos recortados,
   - saltos de línea no deseados,
   - desalineaciones evidentes.

### 5.4. Paso 4: comprobar que el fichero existe y se carga

Regla de oro:

- Si el `.ttf` no se encuentra o no se carga, la aplicación debería fallar con un error claro (no “silencios”).

Esto simplifica mucho el soporte y evita confusión a quien añade estilos.

---

## 6. Recomendaciones de empaquetado (para compartir)

1. Mantén las fuentes en un directorio **propio del proyecto** (ej.: `assets/fonts/`).
2. Conserva licencias por familia en `licenses/` o equivalente.
3. Si publicas en GitHub/PyPI, evita incluir fuentes no redistribuibles del sistema (`/usr/share/fonts/...`)
   o fuentes propietarias (Arial, Verdana, Impact, Consolas).

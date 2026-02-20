# Font equivalence guide and style creation (styles/*.json)

This document explains, step by step, how to replace non-redistributable fonts with freely usable fonts, how we proceeded in our case, and in general how to define new styles inside the styles JSON file.

This guide is intended to work with the existing styles JSON `assets/styles/popup_gui.json`)
where there are references to fonts that are not free, such as `Impact.ttf`, `ariali.ttf`, `Verdana.ttf`, etc.

---

## 1. Context and goal

In the current styles JSON there are styles such as `playful_childlike` and `formal`, with font fields similar to:

- `Tit_FontType` (title)
- `Krn_FontType` (“kernel” / body text)
- `Lbt_FontType` (labels/buttons)
- In the “formal” style, additionally:
  - `hlp_Font`, `hlp_FontBold`, `hlp_CodeFont`

The goal is that all those fields point to free fonts included in the project repository
(so the project is redistributable and reproducible).

---

## 2. What is considered a “font equivalence”

An “equivalence” does not mean the font is identical. It means that:

1. It is **free and redistributable** (with license included).
2. It fulfills a similar role (display / sans / mono / serif).
3. It preserves as much as possible the **layout** (text widths/heights and line breaks) within the project.

In this guide we assume that we already have a flat runtime directory with the final fonts, for example:

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

If your project uses another directory (for example `assets/fonts/`), just copy the `.ttf` files there or adjust
your “asset locator” to search in `fonts_runtime/`.

---

## 3. Recommended substitution table (current JSON cases)

These are the recommended direct substitutions for the names that appear in the current styles JSON:

| Old font (non-redistributable or not desired) | Recommended free substitute                               | Reason / comment                                                 |
| --------------------------------------------- | ----------------------------------------------------------| ---------------------------------------------------------------- |
| `Impact.ttf`                                  | `Anton-Regular.ttf`                                       | Strong display for titles. Practical substitute for Impact.      |
| `ariali.ttf` (Arial Italic)                   | `Arimo-Italic.ttf`                                        | “Arial-like” sans, good metrics compatibility.                  |
| `arialbd.ttf` (Arial Bold)                    | `Arimo-Bold.ttf`                                          | Real bold (no “fake bold”).                                     |
| `Verdana.ttf`                                 | `Inter-Regular.ttf`                                       | Modern UI sans. Stable screen alternative.                      |
| `Verdana_Bold_Italic.ttf`                     | `Inter-BoldItalic.ttf`                                    | Preserves the “title”/emphasis role in the formal style.        |
| `Consolas.ttf`                                | `IBMPlexMono-Regular.ttf`                                 | Modern, redistributable monospaced font.                        |
| `Yrsa-Medium.ttf`                             | `Yrsa-Regular.ttf` *(or `Yrsa-Medium.ttf` if you generate it)* | Free serif. If you need exact “Medium”, generate that instance. |

Notes:

- If your code only uses `pygame.font.Font(path, size)` and does not apply styles afterwards,
  it is preferable to use real static files (`*-Bold.ttf`, `*-Italic.ttf`, etc.).
- Avoid relying on “fake bold / fake italic” (e.g. `set_bold(True)`) if you want layout stability.

---

## 4. Changes made in popup_gui.json to migrate to free fonts

| Style.attribute                 | Previous font           | New free font           |
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

## 5. How to add your own style to the JSON

### 5.1. Step 1: clone an existing style

The safest way is to copy a full block (for example `formal`) and rename the style key:

```json
"my_style": {
  "...": "...",
  "Tit_FontType": "Inter-BoldItalic.ttf",
  "Krn_FontType": "Yrsa-Regular.ttf",
  "Lbt_FontType": "Inter-Regular.ttf"
}
```

### 5.2. Step 2: decide font roles

To keep consistency, decide which family to use for each role:

- **Titles (Tit_)**: display or sans with high weight (e.g. `Inter-Bold.ttf`, `Inter-BoldItalic.ttf`, `Anton-Regular.ttf`).
- **Main text (Krn_)**: readable serif or sans (e.g. `Yrsa-Regular.ttf`, `Inter-Regular.ttf`, `Arimo-Regular.ttf`).
- **Buttons/labels (Lbt_)**: clear and consistent sans (e.g. `Inter-Regular.ttf`, `Arimo-Regular.ttf`).
- **Code (hlp_CodeFont)**: monospaced (e.g. `IBMPlexMono-Regular.ttf`).

### 5.3. Step 3: validate sizes and layout

Practical recommendation:

1. Choose sizes (`*_FontSize`) keeping the current ones.
2. Render a “representative” UI screen.
3. Adjust **only** if you observe:
   - clipped text,
   - unwanted line breaks,
   - obvious misalignments.

### 5.4. Step 4: verify the file exists and loads

Rule of thumb:

- If the `.ttf` cannot be found or loaded, the application should fail with a clear error (no silent fallback).

This greatly simplifies support and avoids confusion for anyone adding styles.

---

## 6. Packaging recommendations (for sharing)

1. Keep fonts in a **project-owned** directory (e.g. `assets/fonts/`).
2. Preserve per-family licenses in `licenses/` or equivalent.
3. If you publish to GitHub/PyPI, avoid including non-redistributable system fonts (`/usr/share/fonts/...`)
   or proprietary fonts (Arial, Verdana, Impact, Consolas).

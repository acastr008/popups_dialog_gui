# Process for obtaining free fonts and generating static TTFs

## 1. Goal

The goal is to replace a set of non-redistributable `.ttf` fonts (e.g., Arial, Verdana, Impact, Consolas) with **free** fonts that can be legally included in an MIT-licensed project, preserving as much as possible the visual behavior and metrics (“layout”) of the project.

The final result provided for use and redistribution is a **flat directory** with static `.ttf` fonts (Regular, Bold, Italic, BoldItalic) that can be loaded in Pygame with:

```python
pygame.font.Font("fonts_runtime/Inter-Regular.ttf", 18)
```

In addition, the corresponding license files are preserved.

---

## 2. Source and rationale

### 2.1. Why “direct download” from fonts.google.com is not used

An automated download method from Google Fonts was attempted using the website’s download endpoint. In practice, this endpoint can return HTML or other responses that are not a valid fonts ZIP in an automated context, which can leave directories empty or incomplete.

For transparency and reproducibility, a more stable source was adopted.

### 2.2. Final source: official `google/fonts` repository

The download is done from the official repository:

- **Repository**: `google/fonts` (GitHub)

This repository contains:
- `.ttf` files (including variable and/or static, depending on the family),
- per-family license text (for example `OFL.txt`, `LICENSE.txt`),
- metadata (`METADATA.pb`) and description (`DESCRIPTION.en_us.html`).

The presence of a per-family license file and the organized repository structure facilitate transparent, auditable usage.

---

## 3. Initial download of font families

### 3.1. Family selection

Free fonts were selected with the goal of covering reasonable substitutes for common non-redistributable fonts and, additionally, providing some “artistic” fonts.

Examples of families used:
- Anton (practical substitute for Impact)
- Arimo (practical substitute for Arial)
- Inter (modern UI substitute, practical alternative to Verdana)
- IBM Plex Mono (substitute for Consolas)
- Yrsa (free serif)
- Various display fonts (Bebas Neue, Lobster, Monoton, Pacifico, etc.)

### 3.2. What was actually downloaded

For each family, the repository typically contains:
- one or more `.ttf` files (sometimes variable with axes, sometimes static),
- `OFL.txt` or `LICENSE.txt`,
- and optional info files (`METADATA.pb`, `DESCRIPTION.en_us.html`).

This download was organized in a working directory with a per-family structure, for example:

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

## 4. Key consideration: variable vs. static fonts

### 4.1. What `[wght]` or `[opsz,wght]` means in the filename

When the filename includes brackets, for example:

- `Arimo[wght].ttf`
- `Inter[opsz,wght].ttf`

it means it is a **variable font**.

Common axes are:
- `wght`: weight (regular/bold/etc.)
- `opsz`: optical size (typographic adjustments depending on size)

### 4.2. Why static fonts are generated

In Pygame, typical usage is to select a specific `.ttf` file:

```python
pygame.font.Font("fonts_runtime/Inter-Bold.ttf", 18)
```

Although Pygame can load a variable font as a normal `.ttf`, it is not practical to rely on internal mechanisms to select typographic axes (weight, optical size). To control the output and facilitate substitutions for fonts such as “Arial Bold” or “Verdana Bold Italic”, it was decided to generate **static instances**.

---

## 5. Generation of final `.ttf` files for distribution

### 5.1. Final structure delivered for runtime use in the project

A flat runtime directory was generated:

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

### 5.2. Generation criteria

The following rules were applied:

#### Families with static fonts already available

If the family includes files such as:
- `Family-Regular.ttf`
- `Family-Bold.ttf`
- `Family-Italic.ttf`
- `Family-BoldItalic.ttf`

they were copied directly into `fonts_runtime/` and renamed to a uniform format:

- `Family-Regular.ttf`
- `Family-Bold.ttf`
- etc.

#### Families with variable fonts

If the family provides variable fonts, 4 static instances are generated:

- Regular    → `wght=400`
- Bold       → `wght=700`
- Italic     → (variable italic file if it exists) with `wght=400`
- BoldItalic → (variable italic file if it exists) with `wght=700`

For `opsz`, a consistent value was set:

- `opsz=14`

This reduces unexpected variations and makes the result more reproducible.

### 5.3. Tool used for instantiation

To convert variable fonts into static instances, the following was used:

- **fontTools** (Python package)

Typical installation:

```bash
pip install fonttools
```

---

## 6. Licenses and traceability

### 6.1. Preserving licenses

For each family, the license files were copied to:

```
fonts_runtime/licenses/<Family>/
```

Without modifying the contents of the license texts.

### 6.2. Generated inventory

An inventory file `fonts_runtime/fonts_runtime.json` was generated containing, for each final `.ttf`:

- family
- style
- final filename
- origin (whether it was copied directly or instantiated from a variable font)
- original source file within the family
- axes used (`wght`, `opsz` if applicable)
- associated licenses

This file makes it possible to audit exactly:
- which original file each final `.ttf` comes from,
- and under which license it is distributed.

### 6.3. Replacement mapping

A file `fonts_runtime/font_replacements.json` was generated with the mapping from old (non-redistributable) names to the new free `.ttf` files.

Typical examples:
- `Impact.ttf` → `Anton-Regular.ttf`
- `ariali.ttf` → `Arimo-Italic.ttf`
- `arialbd.ttf` → `Arimo-Bold.ttf`
- `Verdana.ttf` → `Inter-Regular.ttf`
- `Verdana_Bold_Italic.ttf` → `Inter-BoldItalic.ttf`
- `Consolas.ttf` → `IBMPlexMono-Regular.ttf`
- `Yrsa-Medium.ttf` → `Yrsa-Regular.ttf`

This allows the project to replace old references with paths to `fonts_runtime/*.ttf`.

---

## 7. Warnings and special cases

Some families do not provide 4 real styles. Typical examples:
- Display families that only have Regular (Anton, Bebas Neue, etc.)
- Some artistic fonts do not have a real italic.
- Some families may offer only Bold.

In these cases, transparency is maintained:
- the inventory records which styles actually exist,
- and “fake italics” (artificial oblique) are avoided unless explicitly decided otherwise.

---

## 8. Recommended verification

To validate that the final runtime directory is usable:

1) Check that `.ttf` files exist in `fonts_runtime/`.
2) Load some of them in Pygame (example):
   ```python
   pygame.font.Font("fonts_runtime/Inter-Regular.ttf", 18)
   ```
3) Use `FontViewer.py` to verify visually and review each font’s full JSON.

---

## 9. Result

The result is a set of free, redistributable `.ttf` files, with:
- consistent names,
- a flat directory compatible with typical Pygame usage,
- licenses preserved per family,
- and inventory + mapping that facilitate auditing and replacement in the project.

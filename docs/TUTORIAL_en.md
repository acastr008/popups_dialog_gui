# popups_dialog_gui Tutorial

## Requirements

- Python 3 and `pygame`.

## How to run the demos

- From the project launcher (recommended): select the demo from the list.
- Direct execution: `python3 <demo>.py` (from the project environment).

## Tutorial structure

- Each section corresponds to a demo and describes:
  - what you learn,
  - which API is used,
  - and what result you should observe.

This tutorial presents demos that illustrate different aspects of `popups_dialog_gui`.

First of all, we recommend taking a look at the document **Overview (EN)**: <a href="OVERVIEW_en.md">OVERVIEW_en.md</a>

We will start with an extremely simple demo, meant to validate the most basic functionality of the project.

Then we will continue with a demo that brings together, in itself, demonstrations of the most common features.

The remaining demos are dedicated to illustrating the use of `SurfacePPsct` and the insertion of dynamic surfaces, because their usage
is less trivial and less intuitive. It is only used when we want to include dynamic content inside the popup.

It would even be possible to embed a complete application inside a popup; whether it is convenient requires weighing pros and cons.
In general, it would complicate the code, although it can bring advantages.

Many of the benefits of `popups_dialog_gui` can be obtained with simple usage, without needing dynamic content.

## Demo index

- [1.1) demo_simple.py](#11-demo_simplepy)
- [1.2) demo_Popup_Dialog.py](#12-demo_popup_dialogpy)
- [1.3) demo_Popup_Surface.py](#13-demo_popup_surfacepy)
- [1.4) demo_Popup_Surface_ColorCycle.py](#14-demo_popup_surface_colorcyclepy)
- [1.5) demo_Popup_Surface_Selector.py](#15-demo_popup_surface_selectorpy)
- [2.1) demo_ask_help.py](#21-demo_ask_helppy)
- [2.2) demo_popuphelp_embebido.py](#22-demo_popuphelp_embebidopy)
- [2.3) demo_rebota_controles.py](#23-demo_rebota_controlespy)

---

<a id="11-demo_simplepy"></a>
## 1.1) demo_simple.py

### What you will learn in this demo:

1. Minimal initialization of the popup system over a Pygame window:
   - The main window is created (`pygame.display.set_mode`) and passed to `IniPopupDialog()`.
2. Use of styles (`Style_ID`) as a first customization parameter:
   - The user chooses between 'playful_childlike' and 'formal', and that identifier is applied to the module.
3. Use of a high-level function ready for production:
   - `PopupNOTICE()` shows a modal dialog with a single button, without needing to build classes/sections.
4. Visual context:
   - A background (circles) is drawn to verify that the popup overlays correctly on top of the main rendering.

### API used (core):

- `IniPopupDialog(Display, Style_ID)`
- `PopupNOTICE(Message, IdButt=...)`

### Observable result:

- After choosing a style, you will see the drawn scene and then a NOTICE popup with the selected style and a "Finish" button.

---

<a id="12-demo_popup_dialogpy"></a>
## 1.2) demo_Popup_Dialog.py

<img src="images/1.2_demo_Popup_Dialog.png" alt="1.2 demo_Popup_Dialog" />

This is a very complete demo for using a wide repertoire of very easy-to-use popups.
As in the previous demo (1.1), we start by offering to choose the style type from the terminal.
In the image we can see how it uses `PopupASK()` as a general menu to choose launching small, very simple demos, and also the look of one
of those demos that shows the contents of our source directory.

### What you will learn in this demo:

1. How to use `PopupASK()` to implement menus and decision flows:
   - A menu is nothing more than a “question” with options; the return value is used as a behavior selector.
2. Practical differences between high-level popups:
   - `PopupERR` / `PopupWARN` / `PopupNOTICE` / `PopupINFO` show visual variants for different message types.
3. Interaction cycle based on an application loop:
   - An outer `while True` loop that triggers popups sequentially, avoiding “stacking” windows (modal model).
4. Data preparation for a realistic demo:
   - Generation of a set of files in `/tmp` to test pagination/selection with a large number of elements.
5. File scanning and selection with integrated UI:
   - `PopupScanFiles()` walks a directory and filters by extension (e.g., `.ttf` fonts).
   - `PopupSelectionFiles()` lets you choose a file and returns a path/name for later use.
6. Handling “friendly” paths for UI without breaking internal logic:
   - The absolute path is kept for operations (`PathFonts`), and a shortened version is presented for menu texts.
7. Integration with the project asset locator:
   - `resolve_asset_layout()` centralizes where resources such as `fonts_dir` are and avoids hardcoding paths.

### API used (core):

- `IniPopupDialog(Display, Style_ID)`
- `PopupASK(Message, Buttons, Title=...)`
- `PopupERR(Message)`, `PopupWARN(Message)`, `PopupNOTICE(Message)`, `PopupINFO(Message)`
- `PopupScanFiles(dir=..., extension=...)`
- `PopupSelectionFiles(dir=..., extension=...)`
- `resolve_asset_layout()`  (`fonts_dir`)

### Observable result:

- From the main menu we can launch different kinds of popups. The last two are file demos:
  (i) scanning `.ttf` in the project's fonts directory and (ii) selecting `.txt` in `/tmp` with many elements.
- In the selection option, you can observe the cancellation case (`ret == ''`) and the return case with path/file.

---

<a id="13-demo_popup_surfacepy"></a>
## 2.1) demo_Popup_Surface.py

### What you will learn in this demo:

1. How to insert graphical content (a `pygame.Surface`) as the central “kernel” of a `PopupDialogWindow`:
   - Instead of text (`MessagePPsct`), the main content is a surface drawn by the user.
2. Conceptual relationship with `SurfacePPsct`:
   - The goal is to understand that there is a central section designed to display surfaces (and, in later demos, interactive content).
3. Building reusable surfaces:
   - A surface parameterized by size and title is generated, combining background, shapes, and rendered text.
4. Checking auto-sizing and presentation with varying sizes:
   - Three popups with very different surface dimensions are shown to observe layout behavior.

### API used (core):

- `IniPopupDialog(Display, Style_ID)`
- `PopupDialogWindow(KernelContent, ListIdButt, Title=..., FlagAlert=...)`
- `PopupDialogWindow.Run()`

### Observable result:

- Three popups will be shown in sequence (each with an “Exit” button), where the central area contains a generated image
  with a label indicating the title and size (e.g., “Image 01 (700x200)”).

---

<a id="14-demo_popup_surface_colorcyclepy"></a>
## 2.2) demo_Popup_Surface_ColorCycle.py

### What you will learn in this demo:

1. How to embed “dynamic” content inside the popup's central area using `SurfacePPsct`:
   - Instead of passing a static `pygame.Surface`, you pass an object that implements the `InteractiveContent` lifecycle.
2. How to use a *stub* as a behavior “adapter” to prototype dynamic content:
   - Here *stub* is not used in the classic unit-testing sense, but as a **deliberately simple** component that encapsulates
     a visual behavior (color cycling) so it can be integrated quickly into the popup.
   - This pattern is key because it allows you to:
     - validate the integration **pipeline** (mount → render per frame → unmount) without adding domain complexity,
     - isolate the content logic (what is drawn) from the container (how it is presented and interacted with in the popup),
     - iterate on new “widgets” by changing only this component, keeping the rest of the popup unchanged.
   - In practice, the stub defines three lifecycle hooks:
     - `on_mount(rect)`: prepares resources depending on the assigned size,
     - `draw(surface, rect)`: draws the state on each frame,
     - `on_unmount()`: releases/cleans up resources when closing.
3. Fixed size for interactive content and clipping control:
   - `interactive_size=(600, 350)` forces a consistent size for the interactive “kernel”, useful to validate clipping and layout.
4. Clear separation of responsibilities:
   - The demo defines a “widget” (`ColorCycle`) focused on drawing, while the popup (`PopupDialogWindow`) manages frame, title, and buttons.

### API used (core):

- `IniPopupDialog(Display, Style_ID)`
- `InteractiveContent` (methods: `on_mount()`, `draw()`, `on_unmount()`)
- `SurfacePPsct(content, ..., interactive_size=...)`
- `PopupDialogWindow(kernel_section, ListIdButt, Title=..., FlagAlert=...)`
- `PopupDialogWindow.Run()`

### Observable result:

- A popup opens with the `playful_childlike` style and contains, in its central area, a rectangle colored as a function of time
  and a centered text label “ColorCycle (Step 2)”. The popup closes with the “Close” button.

---

<a id="15-demo_popup_surface_selectorpy"></a>
## demo_Popup_Surface_Selector.py

### What you will learn in this demo:

1. How to build a navigable selector over a collection of surfaces (`pygame.Surface`) using popups:
   - Start from a base list of sizes and titles and transform it into a reusable list of pairs `(surface, ident)`.
2. How to implement “Previous / Next” navigation as a repeated modal flow:
   - A loop keeps the current index and re-opens the popup with the corresponding element, hiding buttons as appropriate
     (start/end of the list).
3. How to parameterize buttons and uniformly resolve the popup return value:
   - Define `labels` dynamically and translate the response from `PopupDialogWindow.Run()` to a button label via
     `resolve_button_label()`, supporting returns such as `str`, `int`, or `dict`.
4. How to use the popup title as the “identifier” of the displayed element:
   - Each surface is accompanied by a string `ident` shown as `Title` and, when selecting, returned as the final result.
5. Demo exit pattern with visual confirmation:
   - After selecting or canceling, the result is drawn on the main window for an interval and the demo ends.

### API used (core):

- `IniPopupDialog(Display, Style_ID)`
- `PopupDialogWindow(KernelContent, ListIdButt, Title=..., FlagAlert=...)`
- `PopupDialogWindow.Run()`

### Observable result:

- A popup opens showing an “image” (surface) and offers buttons to navigate through multiple surfaces.
- If “Select” is pressed, the demo closes the flow and shows the chosen identifier in the main window.
- If “Cancel” is pressed (or it is closed without selection), the demo indicates “Selection canceled.” and ends.

---

## 2.3) demo_Popup_Surface_Selector.py

### What you will learn in this demo:

1. How to build a navigable selector over a collection of surfaces (`pygame.Surface`) using popups:
   - Start from a base list of sizes and titles and transform it into a reusable list of pairs `(surface, ident)`.
2. How to implement “Previous / Next” navigation as a repeated modal flow:
   - A loop keeps the current index and re-opens the popup with the corresponding element, hiding buttons as appropriate
     (start/end of the list).
3. How to parameterize buttons and uniformly resolve the popup return value:
   - Define `labels` dynamically and translate the response from `PopupDialogWindow.Run()` to a button label via
     `resolve_button_label()`, supporting returns such as `str`, `int`, or `dict`.
4. How to use the popup title as the “identifier” of the displayed element:
   - Each surface is accompanied by a string `ident` shown as `Title` and, when selecting, returned as the final result.
5. Demo exit pattern with visual confirmation:
   - After selecting or canceling, the result is drawn on the main window for an interval and the demo ends.

### API used (core):

- `IniPopupDialog(Display, Style_ID)`
- `PopupDialogWindow(KernelContent, ListIdButt, Title=..., FlagAlert=...)`
- `PopupDialogWindow.Run()`

### Observable result:

- A popup opens showing an “image” (surface) and offers buttons to navigate through multiple surfaces.
- If “Select” is pressed, the demo closes the flow and shows the chosen identifier in the main window.
- If “Cancel” is pressed (or it is closed without selection), the demo indicates “Selection canceled.” and ends.

---

# HELP_OPTIONS_TUTORIAL

*Document: options to integrate a help system (Markdown) in Pygame applications with `help_core_pygame` and `popups_dialog_gui`.*

Generation date: **18/Feb/2026 08:30** (Europe/Madrid)

---

## 1. Tutorial goal

These demos show **three complementary patterns** to integrate Markdown help into a Pygame application:

1) **Help as a direct overlay** over the `display` (**`ShowHelpOverlay()`**).  
2) **Help as an embedded popup** within the dialog system (**`PopupHELP()`**).  
3) Integration with **dynamic interactive content** (interactive kernels) and practical considerations:  
   *pause/resume*, `dt` handling, animation freezing, and frame preservation.

The three demos considered “minimal and non-redundant” are:

- `demo_ask_help.py`
- `demo_popuphelp_embebido.py`
- `demo_rebota_controles_ok.py`

---

## 2. Two approaches: `ShowHelpOverlay()` vs `PopupHELP()`

### 2.1 `ShowHelpOverlay(display, md_text, ...)` (help_core_pygame)

**What it is:**  
A help viewer in overlay format **drawn directly onto the `display`**. It is usually **modal** in the practical sense (it captures events until exit),
but it *does not belong* to the popup system.

**Practical implications:**

- It integrates well in simple programs where you do not want to open “another logical window” (another popup), but rather display help on top.
- When closing, you continue in your original flow, but you must take care of:
  - **restoring the previous screen content** (if the overlay leaves its last frame “painted”),
  - the **time step (`dt`)** accumulated while help is open,
  - and if your app has animation, whether you want to **freeze** or **let the simulation run**.

**When it fits best:**

- Applications with their own main loop where you “interrupt” temporarily and then continue.
- Flows like “question → help → back to the question”.
- Programs that do not need help to be a formal “dialog” with style or buttons from the popup framework.

---

### 2.2 `PopupHELP(md_text, ...)` (popups_dialog_gui)

**What it is:**  
A **popup** (dialog window) that contains a Markdown viewer (internally using `help_core_pygame`) as embedded interactive content.

**Practical implications:**

- Help is integrated **as another element of the dialog system**:
  - same style, frame, buttons, layout, etc.
- Since it is a popup, it is natural to treat it as a **modal/blocking** operation relative to the caller popup.
- The recommended pattern when you are already using `PopupDialogWindow` or other popups.

**When it fits best:**

- When you want visual and interaction consistency with the rest of the popups.
- When you want help to “belong” to the dialog system, not as an external overlay.
- When the program is structured around `PopupDialogWindow` and interactive kernels (`InteractiveContent`).

---

## 3. Key considerations (independent of the demo)

### 3.1 Does your application have a general event loop?

There are two typical cases:

#### Case A: **A main loop of your own**

Example: your main `while running:` controls events, updates, and drawing.  
Here you can “enter” help and then return.

- With `ShowHelpOverlay()`: you usually call the function and it manages its own mini modal loop until exit.
- With `PopupHELP()`: you call the help popup, which runs its own interaction and returns when closed.

#### Case B: **Your UI runs inside a `popup.step(events, dt_ms)` loop**

Example: an app organized as a main popup with an interactive kernel.  
Here you typically:

1) detect in your logic that help is requested,  
2) **pause** the main popup,  
3) show help,  
4) when closing, **resume** + control `dt`.

---

### Aside: what `dt` / `dt_ms` is and why it matters when showing help

In game/simulation loops it is common to update state “as a function of the time elapsed since the last frame”.
That elapsed time is often called **`dt`** (*delta time*).

- **`dt`** is usually expressed in **seconds** (float).
- **`dt_ms`** is usually expressed in **milliseconds** (integer).

The idea is that motion and other evolutions depend on real time and not on the number of frames. For example, if an object
moves at 200 px/s, on each frame you advance:

- `dx = speed_px_per_second * dt`  (if `dt` is in seconds)
- or equivalently `dx = speed_px_per_ms * dt_ms` (if you work in milliseconds)

**Typical problem when opening modal help (overlay or popup):** while the user reads the help, real seconds pass.
If your program computes `dt` as “now - last_frame” and you **do not control it**, when you return from help the first `dt`
can be large (e.g., 3000 ms). That causes undesired effects: abrupt animation jumps, unstable physics,
timers expiring all at once, or accumulated simulation steps.

**Practical measures to avoid it:**

1) **Pause** the simulation (or the popup/kernel) before opening help (`pause()`), and resume afterward (`resume()`).
2) When closing help, **reset/discard `dt`** (e.g., with `clock.tick(fps)` or by reinitializing the time reference),
   so the next frame starts with a normal `dt`.

### 3.2 Are there dynamic contents (animation / simulation)?

- If there is NO dynamics, the main risk is **visual**: that when closing the overlay the screen looks “wrong”.
- If there IS dynamics, two additional risks appear:
  1) **The simulation keeps “running”** (or accumulates `dt`) while you are in help.
  2) When you return, the first `dt_ms` can be huge (animation jump).

**Typical best practices:**

- Before opening help, call `pause()` on the main content/popup if it exists.
- When closing help:
  - discard a tick with `clock.tick(fps)` (or reset timers),
  - then call `resume()`.

---

### 3.3 Freeze or not while help is displayed?

This depends on the pattern:

- `ShowHelpOverlay()` is usually modal: **your flow is interrupted** and, if you do nothing, the simulation does not advance because you are inside the overlay.  
  Still, real time passes and **`dt` can accumulate** if you compute it on return.
- `PopupHELP()` (modal) also interrupts the caller flow (as expected).

Default recommendation when there is animation:

- **Freeze** (pause the simulation) while help is visible.
- Resume with a clean `dt`.

---

### 3.4 Restore the frame when closing help?

This is critical for direct overlays:

- If you use `ShowHelpOverlay()` over a `display` that already had a “nice” frame (or a popup drawn),
  when closing the overlay the last overlay frame may remain as background if you do not force an immediate redraw.

Two strategies:

1) **Redraw everything** on return (standard loop).  
2) **Freeze/restore**: keep a copy (`screen.copy()`), show the overlay, and on exit re-blit + `display.flip()`.

The `demo_ask_help.py` demo emphasizes the second.

---

## 4. What the user should take away from each demo

<a id="21-demo_ask_helppy"></a>
### 4.1 `demo_ask_help.py` — “Help as a branch of a dialog”

**What it teaches (technical):**

- Using `PopupASK()` to drive a button-based flow.
- Inserting help with `ShowHelpOverlay()` **without** integrating kernels or creating a help popup.
- Robust visual return: **freeze/restore frame** pattern.

**What you should take away (usage):**

- A typical UX flow:
  - “What do you want to do?” → “Help” → back to exactly the same point.
- Help is a brief interruption and then the main dialog continues.

**Practical lessons:**

- `ShowHelpOverlay()` is ideal for “quick” help in simple flows.
- If you see artifacts after closing help, apply freeze/restore or force a full redraw.

**Didactic summary:**

> “How to add help to a dialog with minimal infrastructure: direct overlay + clean return.”

---

<a id="22-demo_popuphelp_embebidopy"></a>
### 4.2 `demo_popuphelp_embebido.py` — “Help as a formal popup (recommended in the popups ecosystem)”

**What it teaches (technical):**

- A main popup with an interactive kernel (`SurfacePPsct` + `InteractiveContent`).
- Opening help with `PopupHELP()` (help is another popup).
- Pattern `pause()` → open help → `clock.tick()` to discard `dt` → `resume()`.

**What you should take away (usage):**

- If your app is popup-based, help should integrate into the same system:
  - visual consistency,
  - standard interaction,
  - and natural modality within the framework.

**Practical lessons:**

- `PopupHELP()` reduces integration problems because help already “fits” as a dialog.
- Still, with animation you should:
  - pause the main popup,
  - clear `dt` on return.

**Didactic summary:**

> “This is the recommended help pattern when you already use popups: help is a popup, not an external overlay.”

---

<a id="23-demo_rebota_controlespy"></a>
### 4.3 `demo_rebota_controles_ok.py` — “Real case: dynamic kernel + controls + help”

**What it teaches (technical):**

- A more demanding `InteractiveContent`:
  - mouse (LMB/RMB),
  - wheel,
  - keyboard,
  - size changes, pause, and internal state variables.
- Correct separation between:
  - kernel-relative coordinates and
  - `draw()` applying the rect offset.
- Opening `PopupHELP()` from a loop based on `popup.step(...)` without breaking the flow.
- Solid pause/resume management to avoid:
  - animation jumps,
  - `dt` accumulation,
  - input inconsistencies.

**What you should take away (usage):**

- This demo validates the “real” scenario:
  - continuous dynamic content,
  - lots of interaction,
  - and modal help without destroying kernel state.

**Practical lessons:**

- In dynamic kernels, help should be treated as a “modal”:
  - controlled pause,
  - resume with clean `dt`.
- `PopupHELP()` is especially convenient here because it aligns with the framework.

**Didactic summary:**

> “This is the template to integrate help in a real interactive system: input, animation, and modality correctly solved.”

---

## 5. Learning recommendation (suggested order)

1) **`demo_ask_help.py`**  
   Learn the minimal pattern: *direct overlay* + correct return.

2) **`demo_popuphelp_embebido.py`**  
   Learn the recommended pattern within popups: *PopupHELP* + pause/resume.

3) **`demo_rebota_controles_ok.py`**  
   Learn advanced integration: dynamic kernel, controls, and help without side effects.

---

## 6. Implementation checklist (for your own app)

### If you use `ShowHelpOverlay()`

- [ ] Does the screen redraw correctly when returning?
- [ ] If not: do you freeze/restore the frame or force a full redraw?
- [ ] Is there animation? If so:
  - [ ] do you pause the simulation first?
  - [ ] do you clean/discard `dt` on return?

### If you use `PopupHELP()`

- [ ] Is the caller popup paused (`pause()`) before opening help?
- [ ] Do you discard the tick / reset timers on exit?
- [ ] Do you resume (`resume()`) correctly?
- [ ] Should help be consistent with the style of the rest of the popups? (usually yes)

---

## 7. Closing

These last three demos cover **three integration levels**, from less to more structured:

- Direct overlay for “quick” help and simple flows (`ShowHelpOverlay()`).
- Help popup integrated when you already use a dialog framework (`PopupHELP()`).
- Robust integration in dynamic kernels (pause/resume + `dt` handling).

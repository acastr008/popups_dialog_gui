# popups_dialog_gui: (API_REFERENCE_en.md)  Jan 19, 2026

## Structured API listing

### **Module Popup_Dialog.py**

- **Module functions**

  - [DrawRect()](#popup_dialog_py_drawrect)
  - [GetFont()](#popup_dialog_py_getfont)
  - [GetStyleDict()](#popup_dialog_py_getstyledict)
  - [get_style()](#popup_dialog_py_get_style)
  - [set_style_overrides()](#popup_dialog_py_set_style_overrides)
  - [IniPopupDialog()](#popup_dialog_py_inipopupdialog)
  - [TestIni()](#popup_dialog_py_testini)
  - [GetWidthHeigthText()](#popup_dialog_py_getwidthheigthtext)
  - [PopupERR()](#popup_dialog_py_popuperr)
  - [PopupWARN()](#popup_dialog_py_popupwarn)
  - [PopupNOTICE()](#popup_dialog_py_popupnotice)
  - [PopupINFO()](#popup_dialog_py_popupinfo)
  - [PopupASK()](#popup_dialog_py_popupask)
  - [MenuScanFiles()](#popup_dialog_py_menuscanfiles)
  - [MenuSelectFiles()](#popup_dialog_py_menuselectfiles)
  - [GetList_Num_Filenames()](#popup_dialog_py_getlist_num_filenames)
  - [PopupSelectionFiles()](#popup_dialog_py_popupselectionfiles)
  - [PopupScanFiles()](#popup_dialog_py_popupscanfiles)
  - [PopupMens_ERR_WARN_NOTICE_INFO()](#popup_dialog_py_popupmens_err_warn_notice_info)
  - [PopupHELP()](#popup_dialog_py_popuphelp)


### **Module adapters.py**

- **Module functions**

  - [run_help_popup_from_md()](#adapters_py_run_help_popup_from_md)

- **Class - HelpAsInteractive**
  *Adapter that wraps a HelpViewer to behave as InteractiveContent embedded by SurfacePPsct.*

  ***HelpAsInteractive(viewer: Any)***
  - **Methods**
    - [on_mount()](#adapters_py_helpasinteractive_on_mount)
    - [on_unmount()](#adapters_py_helpasinteractive_on_unmount)
    - [update()](#adapters_py_helpasinteractive_update)
    - [draw()](#adapters_py_helpasinteractive_draw)
    - [handle_event()](#adapters_py_helpasinteractive_handle_event)
    - [wants_keyboard()](#adapters_py_helpasinteractive_wants_keyboard)
    - [wants_wheel()](#adapters_py_helpasinteractive_wants_wheel)


- **Class - PopupDialogWindow**
  *The idea behind creating a PopupDialogWindow class is to design an object that simplifies as much as possible the creation of simulated pop-up windows with Pygame.*

  ***PopupDialogWindow(KernelContent: Any, ListIdButt: Any, Title: str = 'Aviso', FlagAlert: str = 'Green', PosCenter: Any = None)***
  - **Methods**
    - [Draw()](#popup_dialog_py_popupdialogwindow_draw)
    - [Run()](#popup_dialog_py_popupdialogwindow_run)
    - [step()](#popup_dialog_py_popupdialogwindow_step)
    - [pause()](#popup_dialog_py_popupdialogwindow_pause)
    - [resume()](#popup_dialog_py_popupdialogwindow_resume)

- **Class - PopupSection**
  *Base class for the different sections that compose a PopupDialogWindow.*

  ***PopupSection(W_Margin: Any, H_Margin: Any, FontType: Any, FontSize: Any, ColorFg: Any, ColorBg: Any, BorderThikness: Any, BorderColor: Any)***
  - **Methods**
    - [Draw()](#popup_dialog_py_popupsection_draw)

- **Class - TitlePPsct**
  *Top section corresponding to the title.*

  ***- TitlePPsct(W_Margin: Any, H_Margin: Any, FontType: Any, FontSize: Any, ColorFg: Any, ColorBg: Any, BorderThikness: Any, BorderColor: Any, TxtTitle: Any)***
  - **Methods**
    - [GetWidthHeigthTitle()](#popup_dialog_py_titleppsct_getwidthheigthtitle)
    - [Draw()](#popup_dialog_py_titleppsct_draw)

- **Class - MessagePPsct**
  *Central section for text.*

  ***MessagePPsct(W_Margin: Any, H_Margin: Any, FontType: Any, FontSize: Any, ColorFg: Any, ColorBg: Any, BorderThikness: Any, BorderColor: Any, Message: Any, PorcSepLines: Any)***
  - **Methods**
    - [GetWidthHeigthMessage()](#popup_dialog_py_messageppsct_getwidthheigthmessage)
    - [Draw()](#popup_dialog_py_messageppsct_draw)

- **Class - ListButtonsPPsct**
  *Bottom section with one or more buttons.*

  ***ListButtonsPPsct(W_Margin: Any, H_Margin: Any, FontType: Any, FontSize: Any, ColorFg: Any, ColorBg: Any, BorderThikness: Any, BorderColor: Any, ListIdButt: Any, ButtPadding: Any, ColorBgBut: Any)***
  - **Methods**
    - [GetWidthHeigthContent()](#popup_dialog_py_listbuttonsppsct_getwidthheigthcontent)
    - [Draw()](#popup_dialog_py_listbuttonsppsct_draw)

- **Class - SurfacePPsct**
  *Central section for the content of a PopupDialogWindow. This content can be a static pygame.Surface or interactive content.*

  ***SurfacePPsct(content_or_surface: Any, W_Margin: Any = None, H_Margin: Any = None, BorderThikness: Any = None, BorderColor: Any = None, *, interactive_size: Any = None)***
  - **Methods**
    - [Draw()](#popup_dialog_py_surfaceppsct_draw)
    - [GetWidthHeigthSurface()](#popup_dialog_py_surfaceppsct_getwidthheigthsurface)
    - [GetWidthHeigthMessage()](#popup_dialog_py_surfaceppsct_getwidthheigthmessage)
    - [update()](#popup_dialog_py_surfaceppsct_update)
    - [handle_event()](#popup_dialog_py_surfaceppsct_handle_event)
    - [wants_keyboard()](#popup_dialog_py_surfaceppsct_wants_keyboard)
    - [wants_wheel()](#popup_dialog_py_surfaceppsct_wants_wheel)

- **Class - HelpPPsct**
  *Central section that embeds a Markdown help viewer (HelpViewer) via `help_core_pygame` and `HelpConfig`.*

  ***HelpPPsct(md_text: Any, interactive_size: Any, W_Margin: Any, H_Margin: Any, BorderThikness: Any, BorderColor: Any, *, title: str = 'Ayuda', style_variant: str = 'formal', style_json_path: Any = None, fonts_dir: Any = None, help_font_file: Any = None, help_code_font_file: Any = None, kernel_bg: Any = None, wheel_step: int = 48, visual_indent_px: int = 24, indent_spaces_per_level: int = 2)***
  - **Methods**
    - [GetWidthHeigthMessage()](#popup_dialog_py_helpppsct_getwidthheigthmessage)
    - [Draw()](#popup_dialog_py_helpppsct_draw)
    - [on_mount()](#popup_dialog_py_helpppsct_on_mount)
    - [on_unmount()](#popup_dialog_py_helpppsct_on_unmount)
    - [update()](#popup_dialog_py_helpppsct_update)
    - [handle_event()](#popup_dialog_py_helpppsct_handle_event)
    - [wants_keyboard()](#popup_dialog_py_helpppsct_wants_keyboard)
    - [wants_wheel()](#popup_dialog_py_helpppsct_wants_wheel)

### **Module interactive_content.py**

- **Class - InteractiveContent**
  *Optional base for interactive/animated content that will be embedded in SurfacePPsct.*

  ***InteractiveContent(*args: Any, **kwargs: Any)***
  - **Methods**
    - [on_mount()](#interactive_content_py_interactivecontent_on_mount)
    - [on_unmount()](#interactive_content_py_interactivecontent_on_unmount)
    - [update()](#interactive_content_py_interactivecontent_update)
    - [draw()](#interactive_content_py_interactivecontent_draw)
    - [handle_event()](#interactive_content_py_interactivecontent_handle_event)
    - [wants_keyboard()](#interactive_content_py_interactivecontent_wants_keyboard)
    - [wants_wheel()](#interactive_content_py_interactivecontent_wants_wheel)

## API inventory summary

### Totals

- **Modules:** 3  
- **Top-level (module) functions:** 22  
- **Classes:** 10  
- **Methods (sum of methods listed per class, excluding constructors):** 43  

### Breakdown by module

#### Popup_Dialog.py

- **Module functions:** 21  
- **Classes:** 8  
- **Methods (in classes):** 29  

#### adapters.py

- **Module functions:** 1  
- **Classes:** 1  
- **Methods (in classes):** 7  

#### interactive_content.py

- **Module functions:** 0  
- **Classes:** 1  
- **Methods (in classes):** 7  

---


## Overview of the main module Popup_Dialog.py

Popup_Dialog_Py.py is a pop-up window module (pop-up) using pygame to generate notices, dialogs, etc.,
and it is based on Pygame.

### Initialization

Before using the module, it is necessary to initialize it by providing
the Pygame display surface and the style to be used.
On top of the chosen style you can apply variations, but they must be made immediately after IniPopupDialog() and before constructing SurfacePPsct/PopupDialogWindow, so that the new
metrics (padding, borders, margins, etc.) are taken into account when measuring
and laying out the sections.

Example:
```
IniPopupDialog(screen, "playful_childlike")
set_style_overrides({
    "Kernel": {"Padding": 0, "Border": 0},
    "Section_Margins": {"Top": 0, "Right": 0, "Bottom": 0, "Left": 0},
})
popup = PopupDialogWindow(...)
```

### General characteristics of the windows

These pop-up windows have three vertically arranged sections and use the PopupDialogWindow() class.
The top section is for the title or to indicate the message type, the next section hosts
the message text, and finally a bottom section with one or more buttons.

The Draw method appears in several classes with different purposes for each of the
three sections mentioned.
Once a section has been rendered, the sections will be arranged appropriately to draw them all
in the top-level class.

```
class PopupDialogWindow:
    class PopupSection: ((aggregation))
        Draw(self):  # definition of the abstract Draw() method for PopupSection

    class TitlePPsct(PopupSection):
        Draw(self, x, y, Wide, Heigth, BorderRadius): # Draws the title section at the top

    class MessagePPsct(PopupSection):
        -.Draw(self, x, y, Wide, Heigth, BorderRadius, PorcSepLines=130): # Draws the central section

    class ListButtonsPPsct(PopupSection):
        -.Draw(self, x, y, Wide, Heigth, BorderRadius): # Draws the bottom section with action buttons
```

### Usage considerations

The main pygame window must be initialized beforehand and will be stored in a global variable 'gameDisplay'.
This design decision was made to avoid having to pass it continuously as a parameter to many functions.

### General notes about the main public functions

- **PopupERR(), PopupWARN(), PopupNOTICE(), PopupINFO():**
These four functions create a PopupDialogWindow and are similar. They are used for different alert levels.
After showing the information, they allow exiting by closing the window via a button.

- **PopupASK():**
This is also a PopupDialogWindow, similar to the previous ones, and requires a list of identifiers to offer several buttons with complete freedom of use.
This lends itself to using these windows not only for typical questions like 'Confirm', 'Cancel', 'Retry', but for any other kind of question, enabling a wide range of functionality.
An immediate example is the possibility of using them to implement a menu, as shown in the Demo.

- **PopupSelectionFiles():**
Based on PopupASK(), a procedure has been implemented that allows selecting files from a directory.
You can force it to consider only files with a given extension. The design is very simple, but even so it supports very long file names and very large directories, because to select a file it allows paging through the list of file names.

---

# Code documentation for the top-level functions

## Popup_Dialog.py — Module functions

<a id="popup_dialog_py_drawrect"></a>
### Popup_Dialog.py — DrawRect(BgColor, BorderColor, Rect, BorderThikness, BorderRadius)
"""Draws a rectangle with fill and (optional) border onto gameDisplay, supporting rounded corners.

**Parameters:**
- BgColor: Fill color (RGB/RGBA or pygame.Color).
- BorderColor: Border color.
- Rect: Target geometry (pygame.Rect or x,y,w,h tuple).
- BorderThikness (int): Border thickness (0 means no border).
- BorderRadius (int): Corner radius (0 means square corners).

**Notes:**
- Requires gameDisplay to be initialized (IniPopupDialog/TestIni).
- Draws the background first and then the border."""

<a id="popup_dialog_py_getfont"></a>
### Popup_Dialog.py — GetFont(FontType, FontSize)
"""Loads and returns a TrueType font using pygame.font.Font.

**Parameters:**
- FontType (str): Path (relative or absolute) to the font file (e.g., *.ttf).
- FontSize (int): Font size in pixels.

**Returns:**
- pygame.font.Font: Font object ready to render text.

**Notes:**
- If the POPUP_PROY_ROOT environment variable exists, it is prepended as the project root.
- Raises an exception if the font cannot be loaded."""

<a id="popup_dialog_py_inipopupdialog"></a>
### Popup_Dialog.py — IniPopupDialog(Display=None, Style_ID=None)
"""Initializes the module: sets the main surface (gameDisplay) and loads the style ST from JSON.

**Parameters:**
- Display: Main pygame.Surface already created (e.g., pygame.display.get_surface()).
- Style_ID (str): Style identifier (e.g., "playful_childlike" or "formal").

**Effects:**
- Defines globals: gameDisplay, Style_id, and ST.
- Loads base style and variants from JSON (if applicable) and validates that Style_ID exists.

**Errors:**
- KeyError if the style does not exist in the loaded JSON files.
- Propagates JSON read/parse errors or path errors.

**Notes:**
- Calls TestIni() at the end to verify minimal coherence.
- If you plan to call set_style_overrides(), do it right after IniPopupDialog() and before creating PopupDialogWindow/SurfacePPsct."""

<a id="popup_dialog_py_get_style"></a>
### Popup_Dialog.py — get_style()
"""Returns the active style dictionary (ST).

**Returns:**
- dict: Active style (same global object).

**Notes:**
- Exposed for reading; modifying it directly will affect rendering.
- For controlled changes, set_style_overrides() is recommended."""

<a id="popup_dialog_py_set_style_overrides"></a>
### Popup_Dialog.py — set_style_overrides(overrides)
"""Applies partial overrides to the active style ST via deep update.

**Parameters:**
- overrides (dict): Partial dictionary whose keys/values are merged onto ST.

**Returns:**
- None

**Notes:**
- Must be called after IniPopupDialog() and before instantiating popups, so that metrics
  (padding, borders, margins) are used correctly when computing sizes."""

<a id="popup_dialog_py_getstyledict"></a>
### Popup_Dialog.py — GetStyleDict()
"""Returns the active style dictionary (ST) as loaded by IniPopupDialog().

**Returns:**
- dict | None: The active style, or None if the module has not been initialized yet.

**Notes:**
- Kept for compatibility; to validate initialization use TestIni().
- The returned dict is the same global object (modifying it affects rendering)."""

<a id="popup_dialog_py_testini"></a>
### Popup_Dialog.py — TestIni()
"""Verifies that the module is initialized and that the minimal style/config is valid.

**Typical validations:**
- Style_id must belong to the supported set.
- gameDisplay must be a valid pygame surface (checked via get_size()).

**Errors:**
- ValueError if the style is not valid.
- Propagates exceptions if the surface is not initialized."""

<a id="popup_dialog_py_getwidthheigthtext"></a>
### Popup_Dialog.py — GetWidthHeigthText(Text, Font, PorcSepLines=130)
"""Computes the size (width, height) of a multi-line text block rendered with a given font.

**Parameters:**
- Text (str): Text with possible newline characters.
- Font (pygame.font.Font): Loaded font.
- PorcSepLines (int): Percentage factor for vertical spacing between lines (e.g., 130).

**Returns:**
- tuple[int, int]: Estimated (width, height) for the text block.

**Notes:**
- Used to size message sections and the popup overall layout."""

<a id="popup_dialog_py_popupmens_err_warn_notice_info"></a>
### Popup_Dialog.py — PopupMens_ERR_WARN_NOTICE_INFO(Message, Title, FlagAlert)
"""Internal popup (not recommended as a stable API) for messages with a single continue button.

**Parameters:**
- Message (str): Message text to display.
- Title (str): Popup title.
- FlagAlert (str): Alert level/color ("Green", "Yellow", "Orange", "Red", "Blue").

**Effects:**
- Creates a modal PopupDialogWindow and blocks until the user presses continue.
- Returns no value ("acknowledge" flow)."""

<a id="popup_dialog_py_popuperr"></a>
### Popup_Dialog.py — PopupERR(Message, IdButt='   Continuar   ', Title='Mensaje de error', FlagAlert='Red')
"""Shows an error popup with a single button.

**Returns:**
- None"""

<a id="popup_dialog_py_popupwarn"></a>
### Popup_Dialog.py — PopupWARN(Message, IdButt='   Continuar   ', Title='Advertencia importante', FlagAlert='Orange')
"""Shows a warning popup with a single button.

**Returns:**
- None"""

<a id="popup_dialog_py_popupnotice"></a>
### Popup_Dialog.py — PopupNOTICE(Message, IdButt='   Continuar   ', Title='Aviso', FlagAlert='Yellow')
"""Shows a notice popup with a single button.

**Returns:**
- None"""

<a id="popup_dialog_py_popupinfo"></a>
### Popup_Dialog.py — PopupINFO(Message, IdButt='   Continuar   ', Title='Mensaje informativo', FlagAlert='Green')
"""Shows an information popup with a single button.

**Returns:**
- None"""

<a id="popup_dialog_py_popupask"></a>
### Popup_Dialog.py — PopupASK(Message, ListIdButt, Title='Pregunta', FlagAlert='Blue')
"""Shows a popup with one or more buttons and returns the pressed label.

**Returns:**
- str: Label/identifier of the pressed button."""

<a id="popup_dialog_py_menuscanfiles"></a>
### Popup_Dialog.py — MenuScanFiles(Page, PageNum, TotNumPages)
"""Builds a paginated (read-only) menu to list files and navigate pages.

**Parameters:**
- Page: List of tuples (num, filename) for the current page.
- PageNum (int): Current page index (0-based).
- TotNumPages (int): Total number of pages.

**Returns:**
- str: Identifier of the pressed button (e.g., " Re.Pag ", " Av.Pag ", or " Finalizar visualización ")."""

<a id="popup_dialog_py_menuselectfiles"></a>
### Popup_Dialog.py — MenuSelectFiles(Page, PageNum, TotNumPages)
"""Builds a paginated menu to select a file by number or navigate between pages.

**Parameters:**
- Page: List of tuples (num, filename) for the current page.
- PageNum (int): Current page index (0-based).
- TotNumPages (int): Total number of pages.

**Returns:**
- str: Pressed button label:
  - " Cancelar " to abort,
  - " Re.Pag " / " Av.Pag " for navigation,
  - or a number ("1", "2", ...) to select the file."""

<a id="popup_dialog_py_getlist_num_filenames"></a>
### Popup_Dialog.py — GetList_Num_Filenames(dir, extension, readable, sort)
"""Gets the numbered list of files in a directory and builds pagination.

**Parameters:**
- dir (str): Directory to scan.
- extension (str | None): Extension filter (without dot) or None for no filter.
- readable (bool): If True, filters for readable files.
- sort (str): Sorting policy (implementation-specific; e.g., 'nd').

**Returns:**
- tuple[list[tuple[int,str]], list[list[tuple[int,str]]]]:
  - List_Num_Filenames: full numbered list (num, filename)
  - listPagesFilenames: list of pages, each with its subset (num, filename)"""

<a id="popup_dialog_py_popupselectionfiles"></a>
### Popup_Dialog.py — PopupSelectionFiles(dir='.', extension=None, readable=True, sort='nd', Title='Seleccionar Fichero', FlagAlert='Blue')
"""Allows selecting a file from the directory using paginated popups.

**Returns:**
- str: Selected filename (including directory) or "" if the user cancels."""

<a id="popup_dialog_py_popupscanfiles"></a>
### Popup_Dialog.py — PopupScanFiles(dir='.', extension=None, readable=True, sort='nd', Title='Seleccionar Fichero', FlagAlert='Blue')
"""Allows browsing (read-only) a directory in paginated mode.

**Returns:**
- None"""

<a id="popup_dialog_py_popuphelp"></a>
### Popup_Dialog.py — PopupHELP(md_text, IdButt='   Cerrar ayuda   ', Title='Ayuda', FlagAlert='Blue', *, interactive_size=(800, 480), W_Margin=None, H_Margin=None, BorderThikness=None, BorderColor=None, title=None, style_variant='formal', style_json_path=None, fonts_dir=None, help_font_file=None, help_code_font_file=None, kernel_bg=None, wheel_step=48, visual_indent_px=24)
"""Shows a popup with an embedded Markdown help viewer as interactive content.

**Dependencies:**
- Requires `help_core_pygame` (HelpViewer + HelpConfig).

**Key parameters:**
- md_text (str): Markdown text to display.
- interactive_size (tuple[int,int]): Logical size of the interactive area (w,h).
- (rest): Kernel margin/border parameters, and HelpViewer configuration.

**Returns:**
- str: Label/identifier of the pressed button (typically the close button)."""

### Popup_Dialog.py — (_private) _deep_update(dst, src) -> None
"""Recursively updates a destination dict with keys from a source dict.

**Notes:**
- Internal utility to merge style overrides.
- Not considered a stable API."""


## Popup_Dialog.py — Classes (constructors and methods)

<a id="popup_dialog_py_popupdialogwindow_init"></a>
### Popup_Dialog.py — PopupDialogWindow.__init__(self, KernelContent, ListIdButt, Title='Aviso', FlagAlert='Green', PosCenter=None)
"""Builds a popup window composed of: title, central kernel, and buttons."""

<a id="popup_dialog_py_popupdialogwindow_draw"></a>
### Popup_Dialog.py — PopupDialogWindow.Draw(self)
"""Draws the complete popup window (frame + sections) onto the main surface."""

<a id="popup_dialog_py_popupdialogwindow_step"></a>
### Popup_Dialog.py — PopupDialogWindow.step(self, events, dt_ms)
"""Processes a non-blocking “tick”: routes events and updates content.

**Returns:**
- str | None: Pressed button label if the dialog is resolved; None if it remains open."""

<a id="popup_dialog_py_popupdialogwindow_run"></a>
### Popup_Dialog.py — PopupDialogWindow.Run(self)
"""Runs the modal loop until the user presses an exit button.

**Returns:**
- str: Label/identifier of the pressed button."""

<a id="popup_dialog_py_popupdialogwindow_pause"></a>
### Popup_Dialog.py — PopupDialogWindow.pause(self)
"""Pauses content updates (if the external loop decides to respect it)."""

<a id="popup_dialog_py_popupdialogwindow_resume"></a>
### Popup_Dialog.py — PopupDialogWindow.resume(self)
"""Resumes content updates (if the external loop decides to respect it)."""


<a id="popup_dialog_py_popupsection_init"></a>
### Popup_Dialog.py — PopupSection.__init__(self, W_Margin, H_Margin, FontType, FontSize, ColorFg, ColorBg, BorderThikness, BorderColor)
"""Base constructor for a popup section: stores style, margins, typography, colors, and border."""

<a id="popup_dialog_py_popupsection_draw"></a>
### Popup_Dialog.py — PopupSection.Draw(self)
"""Abstract rendering method for a popup section."""


<a id="popup_dialog_py_titleppsct_init"></a>
### Popup_Dialog.py — TitlePPsct.__init__(self, W_Margin, H_Margin, FontType, FontSize, ColorFg, ColorBg, BorderThikness, BorderColor, TxtTitle)
"""Creates the top title section and prepares its font."""

<a id="popup_dialog_py_titleppsct_getwidthheigthtitle"></a>
### Popup_Dialog.py — TitlePPsct.GetWidthHeigthTitle(self)
"""Returns the required size (W,H) to render the title with the current style."""

<a id="popup_dialog_py_titleppsct_draw"></a>
### Popup_Dialog.py — TitlePPsct.Draw(self, x, y, Wide, Heigth, BorderRadius)
"""Draws the title section at the top of the popup."""


<a id="popup_dialog_py_messageppsct_init"></a>
### Popup_Dialog.py — MessagePPsct.__init__(self, W_Margin, H_Margin, FontType, FontSize, ColorFg, ColorBg, BorderThikness, BorderColor, Message, PorcSepLines)
"""Creates the central message section, storing the text and line-spacing policy."""

<a id="popup_dialog_py_messageppsct_getwidthheigthmessage"></a>
### Popup_Dialog.py — MessagePPsct.GetWidthHeigthMessage(self)
"""Returns the total size (W,H) required by the message (includes margins and border)."""

<a id="popup_dialog_py_messageppsct_draw"></a>
### Popup_Dialog.py — MessagePPsct.Draw(self, x, y, Wide, Heigth, BorderRadius, PorcSepLines=130)
"""Draws the message section (multi-line text) within the assigned area."""


<a id="popup_dialog_py_listbuttonsppsct_init"></a>
### Popup_Dialog.py — ListButtonsPPsct.__init__(self, W_Margin, H_Margin, FontType, FontSize, ColorFg, ColorBg, BorderThikness, BorderColor, ListIdButt, ButtPadding, ColorBgBut)
"""Creates the bottom button section and prepares its layout."""

<a id="popup_dialog_py_listbuttonsppsct_getwidthheigthcontent"></a>
### Popup_Dialog.py — ListButtonsPPsct.GetWidthHeigthContent(self)
"""Returns the total size (W,H) required by the button area."""

<a id="popup_dialog_py_listbuttonsppsct_draw"></a>
### Popup_Dialog.py — ListButtonsPPsct.Draw(self, x, y, Wide, Heigth, BorderRadius)
"""Draws the bottom section with action buttons."""


<a id="popup_dialog_py_surfaceppsct_init"></a>
### Popup_Dialog.py — SurfacePPsct.__init__(self, content_or_surface, W_Margin=None, H_Margin=None, BorderThikness=None, BorderColor=None, *, interactive_size=None)
"""Builds the central kernel to display a static Surface or interactive content."""

<a id="popup_dialog_py_surfaceppsct_draw"></a>
### Popup_Dialog.py — SurfacePPsct.Draw(self, x, y, Wide, Heigth, BorderRadius=0)
"""Draws the kernel section based on a Surface or interactive content within the assigned area."""

<a id="popup_dialog_py_surfaceppsct_getwidthheigthmessage"></a>
### Popup_Dialog.py — SurfacePPsct.GetWidthHeigthMessage(self)
"""Compatibility alias to obtain the total size of the kernel section."""

<a id="popup_dialog_py_surfaceppsct_getwidthheigthsurface"></a>
### Popup_Dialog.py — SurfacePPsct.GetWidthHeigthSurface(self)
"""Computes the total size required by the SurfacePPsct section."""

<a id="popup_dialog_py_surfaceppsct_update"></a>
### Popup_Dialog.py — SurfacePPsct.update(self, dt_ms)
"""Updates the state of the kernel interactive content, if present."""

<a id="popup_dialog_py_surfaceppsct_handle_event"></a>
### Popup_Dialog.py — SurfacePPsct.handle_event(self, event)
"""Routes events to the interactive content (if present) and returns True if the content consumes them."""

<a id="popup_dialog_py_surfaceppsct_wants_keyboard"></a>
### Popup_Dialog.py — SurfacePPsct.wants_keyboard(self)
"""Indicates whether the kernel wants to receive keyboard events."""

<a id="popup_dialog_py_surfaceppsct_wants_wheel"></a>
### Popup_Dialog.py — SurfacePPsct.wants_wheel(self)
"""Indicates whether the kernel wants to receive mouse wheel events."""


<a id="popup_dialog_py_helpppsct_init"></a>
### Popup_Dialog.py — HelpPPsct.__init__(self, md_text, interactive_size, W_Margin, H_Margin, BorderThikness, BorderColor, *, title='Ayuda', style_variant='formal', style_json_path=None, fonts_dir=None, help_font_file=None, help_code_font_file=None, kernel_bg=None, wheel_step=48, visual_indent_px=24, indent_spaces_per_level=2)
"""Builds the help section that embeds a HelpViewer (Markdown) within the popup."""

<a id="popup_dialog_py_helpppsct_draw"></a>
### Popup_Dialog.py — HelpPPsct.Draw(self, x, y, Wide, Heigth, BorderRadius)
"""Draws the help area (HelpViewer viewport) inside the assigned rectangle."""

<a id="popup_dialog_py_helpppsct_on_mount"></a>
### Popup_Dialog.py — HelpPPsct.on_mount(self, rect)
"""Mount hook: informs the viewer about the absolute rectangle used for rendering and events."""

<a id="popup_dialog_py_helpppsct_on_unmount"></a>
### Popup_Dialog.py — HelpPPsct.on_unmount(self)
"""Unmount hook for the help section (HelpViewer)."""

<a id="popup_dialog_py_helpppsct_update"></a>
### Popup_Dialog.py — HelpPPsct.update(self, dt)
"""Periodic update for the help viewer (kept for cycle homogeneity)."""

<a id="popup_dialog_py_helpppsct_handle_event"></a>
### Popup_Dialog.py — HelpPPsct.handle_event(self, event)
"""Handles Pygame events delegating to the embedded HelpViewer."""

<a id="popup_dialog_py_helpppsct_wants_keyboard"></a>
### Popup_Dialog.py — HelpPPsct.wants_keyboard(self)
"""Indicates whether the help section wants to receive keyboard events."""

<a id="popup_dialog_py_helpppsct_wants_wheel"></a>
### Popup_Dialog.py — HelpPPsct.wants_wheel(self)
"""Indicates whether the help section wants to receive mouse wheel events."""


<a id="popup_dialog_py_interactivecontent_init"></a>
### Popup_Dialog.py — InteractiveContent.__init__(self, *args, **kwargs)
"""Optional base for content embedded in SurfacePPsct."""

<a id="popup_dialog_py_interactivecontent_on_mount"></a>
### Popup_Dialog.py — InteractiveContent.on_mount(self, rect)
"""Stores the absolute rect and marks the content as mounted."""

<a id="popup_dialog_py_interactivecontent_on_unmount"></a>
### Popup_Dialog.py — InteractiveContent.on_unmount(self)
"""Unmount: clears flags and rect."""


## interactive_content.py — Classes

<a id="interactive_content_py_interactivecontent"></a>
### interactive_content.py — InteractiveContent
"""Minimal interface for interactive/animated content (signature definitions)."""

<a id="interactive_content_py_interactivecontent_on_mount"></a>
### interactive_content.py — InteractiveContent.on_mount(self, rect)
"""Called when the content is placed inside the central section."""

<a id="interactive_content_py_interactivecontent_on_unmount"></a>
### interactive_content.py — InteractiveContent.on_unmount(self)
"""Resource cleanup when the content is removed."""

<a id="interactive_content_py_interactivecontent_update"></a>
### interactive_content.py — InteractiveContent.update(self, dt_ms)
"""Periodic update (dt in milliseconds)."""

<a id="interactive_content_py_interactivecontent_draw"></a>
### interactive_content.py — InteractiveContent.draw(self, surface, rect)
"""Draws within 'rect' onto 'surface'."""

<a id="interactive_content_py_interactivecontent_handle_event"></a>
### interactive_content.py — InteractiveContent.handle_event(self, event)
"""Handles one event and returns True if it is consumed."""

<a id="interactive_content_py_interactivecontent_wants_keyboard"></a>
### interactive_content.py — InteractiveContent.wants_keyboard(self)
"""Indicates whether it wants keyboard events."""

<a id="interactive_content_py_interactivecontent_wants_wheel"></a>
### interactive_content.py — InteractiveContent.wants_wheel(self)
"""Indicates whether it wants mouse wheel events."""


# Final notes

- Depends on Pygame; execution requires an initialized display (pygame.display).
- Uses global state (global statements); it is advisable to initialize the module via a dedicated method.
- Includes forced exits (sys.exit), which may be undesirable when integrated as a library.
- Loads styles from JSON files using relative paths; path resolution depends on the current working directory.
- The code contains 'BUG' comments that indicate known behaviors to review.
- Detected imports: pygame, sys, time, os, os.path, pygame_widgets, json, pygame_widgets.textbox.TextBox, help_core_pygame.help_core.HelpViewer, help_core_pygame.help_core.HelpConfig, pathlib.Path
- Globals declared: gameDisplay, Style_id, ST
- Contains TODOs; there is planned functionality not yet implemented.

---

## adapters.py - Functions and classes

<a id="adapters_py_helpasinteractive"></a>
### adapters.py - HelpAsInteractive
"""Wraps a `HelpViewer` so it can be embedded as interactive content inside `SurfacePPsct`.

Implements the minimal interface expected by the popup event router:
- on_mount / on_unmount
- update
- draw
- handle_event
- wants_keyboard / wants_wheel
"""

<a id="adapters_py_helpasinteractive_on_mount"></a>
### adapters.py - HelpAsInteractive.on_mount(self, rect)
"""Receives the kernel usable rectangle (pygame.Rect) and forwards it to the viewer if supported."""

<a id="adapters_py_helpasinteractive_on_unmount"></a>
### adapters.py - HelpAsInteractive.on_unmount(self)
"""Unmount hook (kept for interface compatibility)."""

<a id="adapters_py_helpasinteractive_update"></a>
### adapters.py - HelpAsInteractive.update(self, dt)
"""Periodic update (dt in ms). Default: no-op (the viewer is typically static)."""

<a id="adapters_py_helpasinteractive_draw"></a>
### adapters.py - HelpAsInteractive.draw(self, surface, rect)
"""Draws the viewer inside the given rect delegating to `HelpViewer.draw(surface, rect)`."""

<a id="adapters_py_helpasinteractive_handle_event"></a>
### adapters.py - HelpAsInteractive.handle_event(self, event)
"""Forwards pygame events to the viewer and returns True if the viewer consumes them."""

<a id="adapters_py_helpasinteractive_wants_keyboard"></a>
### adapters.py - HelpAsInteractive.wants_keyboard(self)
"""Indicates that this content wants keyboard events."""

<a id="adapters_py_helpasinteractive_wants_wheel"></a>
### adapters.py - HelpAsInteractive.wants_wheel(self)
"""Indicates that this content wants mouse wheel events."""

<a id="adapters_py_run_help_popup_from_md"></a>
### adapters.py - run_help_popup_from_md(md_text, *, title="Help", interactive_size, ...)
"""Convenience helper: builds a `HelpViewer` from Markdown, adapts it as interactive content,
and displays it inside a `PopupDialogWindow`.

**Notes:**
- Call after `IniPopupDialog(...)`.
- Normalizes the typical flow: `HelpViewer` -> `HelpAsInteractive` -> `SurfacePPsct` -> `PopupDialogWindow.Run()`.
"""

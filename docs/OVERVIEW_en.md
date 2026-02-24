# popups_dialog_gui: (OVERVIEW_en.md)  11/Jan/2026

## Description of the different modules

### Popup_Dialog.py

It is a **popup windows module** (pop-up) using Pygame to generate notices, dialogs, etc., and also some more advanced possibilities. It is based on Pygame.

This is not about emulating a complete GUI toolkit such as TkInter, GTK, or anything similar. The goal is to offer some basic graphical user interface (GUI) features while always using PyGame as the base, because advanced GUIs do not always mix well with other graphics environments.

This happens with Pygame and is usually because they do not share event management and certain low-level system graphics resources well. When you try to mix, for example, PySide6 or Tkinter with Pygame, both frameworks try to control the event loop (mouse/keyboard input and window updates). SDL2, used by Pygame, puts its events in its own queue; Qt or Tkinter do the same in theirs. If you start two “main loops” in the same process, events may remain unprocessed or windows may not close properly, and sometimes SDL2 subprocesses remain open because they were left referenced by internal C structures.

SDL2 provides you with a cross-platform API (Linux, Windows, macOS, even consoles or mobile) to create windows, draw pixels or textures on screen, play sound, and capture input events. Pygame does not reimplement all of that in Python; instead it wraps it (bindings) over SDL2, so you work with Python classes and functions but the real engine runs in C/C++.

The purpose of popups_dialog_gui is to complement Pygame by providing a set of features that are not included in Pygame and are very useful for many programs on this platform. There are several Python libraries with the same goal but with different approaches, and they can be complementary in practice.

Beyond some basic functionality for a set of frequently used standard windows, some more advanced options have been provided that allow embedding interactive content. For that, it was necessary to include a couple of additional modules, described below.

### Interactive_content.py

A module that defines the **contract and runtime** for embeddable interactive content (events, draw, sizing, focus, wheel, etc.).

### adapters.py

A module that defines **integrations** (wrappers/bridges) between external systems (e.g., `HelpViewer`) and that contract (e.g., “Help as InteractiveContent”).

## General characteristics of the windows

These elements that we call (perhaps somewhat pretentiously) pop-up windows in popups_dialog_gui behave as if they were pop-up windows, but they are not. In reality, they are simulated windows, because in Pygame there is only one main window for the whole application.

The key simplification in this type of simulated window is that once opened, it cannot be moved or resized. This is not a big problem, but one consequence is that after initialization with a given window style (fonts, colors, thicknesses and margins, etc.), it can no longer be modified, because the window was automatically sized based on its content from the start. This makes it much easier to use. From now on we will refer to them simply as windows, omitting the “fake” part.

The style of these windows is configurable. For now, a couple of styles have been implemented.

We use **modal** pop-up windows. That is, in principle they will block interaction with the rest of the application until the pop-up window is closed. However, as explained earlier, the InteractiveContent class has been implemented as an extension in the interactive_content.py module. This allows us to manage interactive content inside a pop-up window.

This last advanced possibility requires a type of usage that is not as trivial as the more common uses for simple messages or pop-up dialogs.

The point is that with popups_dialog_gui we can use these windows, with these limitations, for a wide number of common situations while providing very interesting and necessary functionality in many circumstances.

These pop-up windows have three sections arranged vertically and use the PopupDialogWindow() class. They are automatically sized to accommodate the texts with the fonts indicated in each of the three sections. The widest section of the three determines the total width of the window.

1. The top section for the title or to indicate the message type.
2. The next one is a central section that holds the message text or other kinds of content.
3. Finally, there is a bottom section with one or more buttons.

## The best way to learn how to use popups_dialog_gui is to check the demos

The best starting point is our [TUTORIAL_en.md](TUTORIAL_en.md), which helps you go through a series of tutorials to practice with a variety of examples explaining its usage and how it works.

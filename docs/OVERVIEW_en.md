# popups_dialog_gui: (OVERVIEW_en.md)  11/Jan/2026

## Description of the different modules

### Popup_Dialog.py

It is a **pop-up windows module** using Pygame to generate notices, dialogs, etc., and also some more advanced possibilities. It is based on Pygame.

This is not intended to emulate a complete GUI toolkit such as TkInter or GTK, or anything similar.
What is attempted is to offer some basic graphical user interface (GUI) functionality while always using PyGame as the base, because advanced GUIs do not always combine well with other graphical environments.

This happens with Pygame and generally it is because they do not share event management well and certain low-level graphical system resources.
The proposal of `popups_dialog_gui` is to serve as a complement to provide Pygame with a set of functionalities that are not included in Pygame, and that are very useful for many programs on this platform.

In addition to some basic functionality for a set of standardized, frequently used windows, some more advanced options have been provided that allow embedded interactive contents to be used.
For that, it was necessary to include a couple of additional modules, which are detailed below.

### Interactive_content.py

It is a module that defines the **contract and the runtime** for embeddable interactive content (events, draw, sizing, focus, wheel, etc.).

### adapters.py

It is a module that defines **integrations** (wrappers/bridges) between external systems (e.g., `HelpViewer`) and that contract (e.g., “Help as InteractiveContent”).

## General characteristics of the windows

These elements that we call (perhaps pretentiously) pop-up windows of `popups_dialog_gui` behave as if they were pop-up windows, but they are not.
In reality, they are simulated windows since in Pygame there is only one main window for the entire application.

The key simplification in this type of simulated windows is that once they have been opened, they cannot be moved or resized.
It is not really a big problem, but one of the consequences of this is that after initialization with a given window style (fonts, colors, thicknesses and margins, etc.), it can no longer be modified, because the window was automatically sized according to its content from the start.
This makes it much easier to use. From now on we will refer to them simply as windows, omitting the “fake” part.
The style of these windows is configurable. For now, a couple of styles have been implemented.

We use modal pop-up windows. That is, in principle they will block interaction with the rest of the application until the pop-up window is closed.
However, as explained before, the `InteractiveContent` class has been implemented as an extension in the `interactive_content.py` module. This allows us to manage interactive contents inside a pop-up window.
This advanced possibility requires a usage pattern that is not as trivial as the most common uses for simple messages or pop-up dialogs.

The fact is that with `popups_dialog_gui` we can make use of these windows with these limitations for a wide number of common situations, providing very interesting and necessary functionality in many circumstances.

These pop-up windows have three sections arranged vertically and make use of the `PopupDialogWindow()` class, and they will be automatically sized to accommodate the texts with the fonts indicated in each of the three sections. The widest of the three sections will determine the total width of the window.

1. The top section for the title or to indicate the message type.
2. Next, a central section that will contain the message text or other kinds of content.
3. Finally there will be a bottom section with one or more buttons.

## The best way to learn how to use popups_dialog_gui is to review the demos

The best thing is to go to our [TUTORIAL_en.md](TUTORIAL_en.md), which helps us move through a series of tutorials to practice with a variety of examples, explaining their usage and how they work.

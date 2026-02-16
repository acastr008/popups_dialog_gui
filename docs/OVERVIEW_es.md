# popups_dialog_gui: (OVERVIEW_es.md)  11/ene/2026

## Descripción de los diferentes módulos

### Popup_Dialog.py

Es un **módulo de ventanas emergentes** (pop-up) usando Pygame para  generar  avisos, diálogos, etc.,  y tambien algunas posibilidades más avanzadas. Está basada en Pygame. 

No se trata de emular un toolkit completo para GUI del tipo TkInter, o un GTK, ni nada parecido. 
Lo que se intenta es ofrecer algunas funcionalidades básicas tipo graphical user interface (GUI) siempre usando PyGame como base, porque no siempre los GUIs avanzados combinan bien con otros entornos gráficos. 

Esto ocurre  con Pygame y generalmente se debe a que  comparten mal la gestión de eventos y ciertos recursos gráficos del sistema a bajo nivel. 
La propuesta de popups_dialog_gui es servir de complemento para dotar a Pygame de una serie de funcionalidades  que no se incluyen en Pygame, y que vienen muy bien para muchos programas en esta plataforma.
Aparte de algunas funcionalidades básicas para una serie de ventanasa estandarizadas de uso frecuent, se han proporcionado algunas opciones más avanzadas que permiten usar contenidos interactivos embebibles.
Para ello fue necesario incluir un par de módulos adicionales que se detallan a continuación. 

### Interactive_content.py

Es un módulo que define el **contrato y el runtime** de contenido interactivo embebible (eventos, draw, sizing, foco, wheel, etc.).

### adapters.py

Es un módulo define **integraciones** (wrappers/puentes) entre sistemas externos (p. ej. `HelpViewer`) y ese contrato (p. ej. “Help como InteractiveContent”

## Caraterísticas generales de las ventanas

Estos elementos que denominamos (quizás pretenciosamente) ventanas emergentes de popups_dialog_gui, se comportan como si fueran ventanas emergentes (pop-up), pero no lo son.
En realidad, son ventanas simuladas ya que en Pygame solo hay una ventana principal para toda la aplicación. 

La simplificación clave en este tipo de ventanas simuladas, es que que una vez que se han abierto, no se pueden ni trasladar ni redimensionar. 
Realmente no es un gran problema, pero una de las consecuencias de ello, es que tras la inicializacion con un determinado estilo de ventana, (fuentes, colores, grosores y márgenes, etc.), ya no se puede modificar, porque la ventana se dimensionó automáticamente en funcion de su contenido desde el inicio. Esto facilita mucho su uso. En lo sucesivo nos  referiremos a ellas como ventanas obviando lo de falsas.
El estilo de estas ventanas es configurable. Por el momento se han implementado un par de estilos.

Usamos ventanas emergentes Modales. Es decir, en principio bloquearán la interacción con el resto de la aplicación hasta que se cierre la ventana emergente. No obstante, tal como se explicó antes, se ha implementado a modo de extensión la clase InteractiveContent en el módulo interactive_content.py. Esto nos permite gestionar contenidos interactivos dentro de una ventana pop-up.
Esta última posibilidad avanzada, exije un tipo de uso que no resulta tan trivial como los usos más habituales para simples mensajes o diálogos emergentes.

El caso es que con popups_dialog_gui conseguimos hacer uso de estas ventanas con estas limitaciones para un amplio número de situaciones comunes aportando funcionalidades muy interesantes y necesarias en multitud de circunstancias. 

Estas ventanas pop-up tienen tres secciones dispuestas verticalmente y hacen uso de la clase PopupDialogWindow() y se dimensionarán automáticamete para dar cabida a los textos con las fuentes indicadas en cada una de las tres secciones. La msección más ancha de las tres condicionará la anchura total de la ventana.

1. La sección superior para el título o para indicar el tipo de mensaje.
2. La siguiente es una sección central que dará cabida al texto del mensaje o a otro tipo de contenidos 
3. Finalmente existira una sección inferior con uno o más botones.
   
## La mejor forma de aprender a usar popups_dialog_gui es consultar las demos

Lo mejor es acudir a nuestro [TUTORIAL_es.md](TUTORIAL_es.md) que nos ayuda a transitar por una serie de tutoriales para practicar con una vaierdad de ejemplos explicando su uso y su funcionamiento.

 

**Nota:** _Esta entrega se evalúa en el laboratorio, con todos los integrantes del grupo presentes._

# Entrega 2 del proyecto robot móvil.

En el caso de un robot móvil, éste deberá poder moverse con autonomía de un punto a otro de un espacio definido por el profesor, usará sensores y efectores al ubicarse y trasladarse, así como programas para tomar decisiones.
Aunque será autónomo, el robot podrá intercambiar información con el entorno. En esa interacción, el robot podrá usar texto, sonidos, imágenes estáticas y animaciones, así como sensores y efectores necesarios para tales fines. Al comenzar a ejecutar las funciones de esta entrega, los créditos de los integrantes del grupo deberán darse a conocer, con el fin de tener claro a quiénes pertenece el robot.

No será necesario el uso de claves para que el robot funcione.
La entrega formal consistirá en colocar en el sitio del curso en Mediación Virtual  el código que maneje al robot y el respectivo robot deberá ejecutar las funciones asignadas en el laboratorio en el recinto.
El material entregado deberá cumplir con lo siguiente:

## Requisitos

 1. El robot debe funcionar correctamente en un kit  disponible en el recinto.
 2. Los programas (código) del robot deberán poder ser variados y reinstalados en él, así como otros programas también podrán ser instalados en él con el fin de cumplir adicionales o nuevas funciones que esté en capacidad mecánica, eléctrica y electrónica de desempeñar. Los programas podrán ser revisados por el profesor en el momento en que él lo pida, durante o después de la presentación de la entrega.
 3. El robot y sus programas ejecutarán las siguientes funciones y cumplirán con los siguientes requisitos:
	1. Usar los sensores de contacto, luz, sonido (micrófono), ultrasonido, giro y tiempo. Los dos últimos tienen que ver con los motores.
	2. Usar conexión de Bluetooth
	3. Usar al menos dos motores.
	4. Contar con suficiente energía para cumplir las tareas asignadas.
	5. Usar la velocidad apropiada para desempeñar las tareas, de manera que no ponga en riesgo la seguridad del kit de robótica ni dure demasiado tiempo haciendo las tareas encomendadas.
	6. Usar el modelo planteado en la entrega 1 del proyecto 2, con los cambios autorizados por el profesor.
	7. Con ese modelo, hacer lo que se detalla a continuación
		1. Desplazarse en línea recta hacia adelante tres segundos. :white_check_mark:
		2. Desplazarse hacia atrás a la posición inicial. :white_check_mark:
		3. Desplazarse y con el sensor de luz seguir  una línea negra pintada sobre una superficie blanca hasta encontrar un obstáculo por medio de sensor de contacto y empujarlo 10 cms en ángulo de 45 grados en relación con la dirección que el robot llevaba y detener. :warning:
		4. Desplazarse y seguir un foco que tendrá la luz encendida; si la luz se apaga, el robot se detiene, de lo contrario la busca. Esto se hará con la luz del laboratorio apagada. Si el robot escucha un sonido (en una o varias ocasiones), emitirá una secuencia de frecuencias y dará marcha atrás tres segundos a pesar de percibir la luz o si no la percibe. Después, podrá seguir la luz otra vez. :warning:
		5. Desplazarse en línea recta hacia adelante al escuchar un sonido, detectar por medio de sensor de contacto una barrera que estará en su ruta, cambiar la ruta y evadir el obstáculo para detenerse 10 cms. después de superarlo y devolverse solo a su punto de partida. :construction:
		6. Desplazarse en línea recta hacia adelante y si encuentra el fin o borde de la mesa donde está o un abismo o precipicio, evitarlo, no caer en él. :construction:
		7. Desplazarse, detectar por medio de sensor de ultrasonido una barrera que estará en su ruta, cambiar la ruta y evadir el obstáculo bordeándolo para  superarlo y recuperar la dirección o ruta que llevaba hasta encontrar una bola roja y detenerse ante ella. :construction:
		8. Por medio de Bluetooth, el robot recibirá un mensaje desde un computador y lo desplegará en la pantalla del "ladrillo". :construction:
		9. El robot podrá portar un marcador o un lápiz y dibujará un cuadrado de 10 cms. de lado. :warning:
		10. El robot dirá los nombres de sus creadores. :construction:

## Opcionales

1. Usar el sensor termómetro si está en su kit y si tiene el cable conversor de sensores RCX a NXT, de manera que el robot se aleje al contacto con el calor.
2. Usar emisor y receptor de luz infrarroja para que el robot camine hacia atrás.
3. Usar el sensor de color para clasificar bloques de Lego de diferentes colores.


## En general se revisa

- que el robot cumpla con todas las tareas asignadas
- que las tareas asignadas al robot sean desempeñadas apropiadamente
- que para efectuar las tareas, el robot utilice apropiadamente sensores, efectores y programas solicitados por el profesor
- si el robot puede interactuar con el entorno
- la estructura del robot y de los programas que lo gobiernan
- si en el robot se aplicaron cosas llamativas o novedosas y se incluyeron funciones no pedidas que trabajan bien
- si la información eventualmente emitida por el robot se puede percibir, entender y usar bien
- si el tiempo usado para realizar cada tarea es aceptable o muy lento o más bien demasiado rápido
- si es fácil manipular el robot y ponerlo a funcionar
- si el robot se desarma antes, mientras o después de efectuar las tareas asignadas
- si el robot se detiene o deja de funcionar debido a errores de programación
- si el robot no ejecuta bien las tareas porque no está ajustado a las condiciones del entorno (iluminación, terreno u otros)
- si usó  alguna técnica de inteligencia artificial
- la puntualidad en la entrega

## Atrasos

Cada día de atraso en una entrega implica una multa o rebajo de la décima parte del valor total de esa entrega. Por ejemplo, si en  la entrega un grupo obtiene nota  8  de  10%, pero con un retraso de tres días, el cálculo es (0.8 x 10)-(3 x 1.0)= 8-3=5% en lugar  de 10% que vale la entrega.


## Referencias

- [http://www.philohome.com/sensors/tempsensor.htm](http://www.philohome.com/sensors/tempsensor.htm)
- [http://www.convict.lu/Jeunes/ultimate_stuff/Making%20your%20own%20RCX%20sensors.pdf](http://www.convict.lu/Jeunes/ultimate_stuff/Making%20your%20own%20RCX%20sensors.pdf)
- [http://www.dexterindustries.com/howto/lego-mindstorms-motors-with-raspberry-pi-brickpi-0-1/](http://www.dexterindustries.com/howto/lego-mindstorms-motors-with-raspberry-pi-brickpi-0-1/)
- [http://courses.washington.edu/engr100/Section_Wei/NXT/tricks.pdf](http://courses.washington.edu/engr100/Section_Wei/NXT/tricks.pdf)
- [http://www.nt.ntnu.no/users/skoge/prost/proceedings/ifac2014/media/files/1821.pdf](http://www.nt.ntnu.no/users/skoge/prost/proceedings/ifac2014/media/files/1821.pdf)
- [http://nebomusic.net/NXT-G-BasicLineFollow.html](http://nebomusic.net/NXT-G-BasicLineFollow.html)
- [http://www.coertvonk.com/family/school/lego-mindstorms-nxt-g-6107](http://www.coertvonk.com/family/school/lego-mindstorms-nxt-g-6107)
- [http://courses.washington.edu/engr100/Section_Wei/NXT/tricks.pdf](http://courses.washington.edu/engr100/Section_Wei/NXT/tricks.pdf)
- [http://www.rocwnc.org/Beginning_NXT_Programming_Workshop.pdf](http://www.rocwnc.org/Beginning_NXT_Programming_Workshop.pdf)
- [http://www.kirp.chtf.stuba.sk/moodle/pluginfile.php/46109/mod_resource/content/1/Lego%20Mindstorms%20NXT-G%20programming%20guide.pdf](http://www.kirp.chtf.stuba.sk/moodle/pluginfile.php/46109/mod_resource/content/1/Lego%20Mindstorms%20NXT-G%20programming%20guide.pdf)
- [http://www.legoengineering.com/wp-content/uploads/2013/06/download-tutorial-pdf-2.4MB.pdf](http://www.legoengineering.com/wp-content/uploads/2013/06/download-tutorial-pdf-2.4MB.pdf)

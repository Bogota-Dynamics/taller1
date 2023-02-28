# Taller 1

## Integrantes

- Tony Santiago Montes
- Sebastián Guerrero
- Maria Fernanda Tarquino
- Santiago Rueda

## Setup del proyecto

Para poder ejecutar todos los pasos de este taller exitosamente, asegúrese de haber hecho primero los siguientes pasos:

0. Tener instalado por completo ROS2 y haber creado un workspace.
1. Instalar CoppeliaSim y reemplazar el archivo `libsimExtROS2.so` en la carpeta `utils`; poner a correr el archivo `coppeliaSim.sh` y abrir la escena `taller_1.ttt` de la carpeta `utils`.
2. Descargar el paquete anexo `my_msgs` y ponerlo en la carpeta `src` del workspace.
3. Construir ambos paquetes con los siguientes comandos en terminal (en la carpeta raíz del workspace):

```bash
colcon build --packages-select my_msgs
colcon build --packages-select taller1
```

**NOTA: Asegúrese de ejecutar todos los comandos en la carpeta raíz del workspace**, de lo contrario el archivo del recorrido del robot no se guardará en la carpeta correspondiente y obtendrá un error.

## Pasos para correr cada punto del proyecto

### Punto 1. Operar el robot mediante el teclado

En una terminal corra el nodo `/turtle_bot_teleop` mediante los comandos:

```bash
. install/setup.bash
ros2 run taller1 turtle_bot_teleop
```

Se le preguntará por la velocidad lineal y angular del robot, digite dos valores enteros positivos deseados (e.i. 4).

Posteriormente, ponga a correr la simulación en CoppeliaSim y presione cualquiera de las teclas w,a,s,d que moverán al robot de la siguiente forma:
- `w`: Adelante
- `a`: Izquierda
- `s`: Atrás
- `d`: Derecha

*Tenga en cuenta que el robot de la simuilación lleva cierta incercia del movimiento, por lo cual no se detendrá inmediatamente al dejar de presionar la tecla, sino que se deslizará un poco antes*

### Punto 2. Mostrar en una interfaz la posición y recorrido del robot

En una nueva terminal corra el nodo `/turtle_bot_interface` mediante los comandos:

```bash
. install/setup.bash
ros2 run taller1 turtle_bot_interface
```

Esto abrirá una nueva ventana con una interfaz con dos botones, un título (por defecto "Robot") y un recuadro. *Tenga en cuenta que la interfaz no se mostrará ni funcionará mientras la simulación no se esté corriendo.*

Mediante los mismos comandos (y mientras tenga la terminal del punto 1 en ejecución) se moverá el robot en la simulación y su movimiento se graficará en la interfaz.

También puede guardar la gráfica del recorrido realizado por el robot, mediante el botón `Guardar Imagen`, esto abrirá una ventana para seleccionar donde desea guardar la imagen y el nombre que desea ponerle.

### Punto 3. Guardar el recorrido del robot en un archivo TXT

Dado que el servicio `save_motion` que se encarga de guardar el archivo TXT del recorrido del robot fue creado dentro del nodo `/turtle_bot_teleop` que ya se encuentra en ejecución, no es necesario correr ningún nodo adicional, simplemente es necesario que estén corriendo los nodos de los 2 puntos anteriores.

Con esto podrá cambiar el título de la gráfica (será el nombre del archivo TXT) y posteriormente presionar el botón `Guardar Recorrido` de la interfaz, lo cual guardará automáticamente el archivo TXT con el título de la gráfica en la carpeta `motion` del taller1.

### Punto 4. Recrear el recorrido del robot desde un archivo TXT

Finalmente, para recrear un recorrido de un archivo TXT guardado en el punto anterior, debe abrir una nueva terminal y correr el nodo `/turtle_bot_player` mediante los comandos:

```bash
. install/setup.bash
ros2 run taller1 turtle_bot_player
```

Este nodo implementa el servicio `recreate_motion`, por lo cual no se deplegará nada en pantalla hasta que se llame el servicio.

Posteriormente, reinicie la simulación en CoppeliaSim y en otra consola llame el servicio expuesto por el nodo player, en donde indicará el nombre del recorrido guardado que desea recrear (e.i. "Robot"). Para llamar el servicio ejecute el siguiente comando, reemplazando "Robot" por el nombre de la gráfica que tenía el recorrido que guardó.

```bash
ros2 service call /recreate_motion my_msgs/srv/SaveMotions '{filename: "Robot"}'
```

Si todo está correctamente configurado, observará que en la consola del nodo `/turtle_bot_player` se ejecuta cada una de las acciones realizadas en el nodo `/turtle_bot_teleop` incluyendo el tiempo que haya durado detenido entre cada cambio de tecla con el fin de recrear con mayor precisión el recorrido. Asimismo, observará que en la simulación, el robot realiza el recorrido siguiendo los mismos comandos recreados.

**Tenga en cuenta que debido a la incercia del robot y su leve inclinación inicial, el recorrido *siempre* va a variar aunque sea un poco, a pesar de que las instrucciones  y la velocidad sean exactamente las mismas.**

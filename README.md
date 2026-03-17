# Simulación Interactiva de Tela en Python y Pygame

<span><img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue"/></span>

Este script implementa una **simulación interactiva de una tela o malla suspendida**, desarrollada en **Python** con **Pygame**. La escena representa una red de celdas cuadradas colgada de varios puntos de anclaje en su borde superior. A medida que esos puntos se desplazan, la estructura se deforma y adopta nuevas formas de caída, generando un comportamiento visual similar al de una **tela liviana** o una **red flexible**.

![Posición inicial de la simulación.](https://github.com/VintaBytes/Simulacion-Interactiva-de-Tela-en-Python-y-Pygame/blob/main/imagen0.png)

Además de la deformación dinámica, **el programa permite rasgar la malla con el mouse**. Mientras el botón izquierdo permanece presionado, el cursor actúa como una herramienta de corte que elimina conexiones entre nodos cercanos. Esto produce desgarros en tiempo real, fragmentando la estructura y alterando su comportamiento físico de manera inmediata.

![Malla con algunos cortes.](https://github.com/VintaBytes/Simulacion-Interactiva-de-Tela-en-Python-y-Pygame/blob/main/imagen1.png)

Desde el punto de vista técnico, la simulación está basada en un **modelo discreto de partículas y restricciones**. Cada intersección de la malla se representa como un punto con posición actual y posición anterior. Los puntos libres son afectados por la gravedad, mientras que ciertos puntos de la fila superior actúan como anclajes fijos o controlables por el usuario.

La actualización del movimiento se realiza mediante integración de **Verlet**, una técnica muy utilizada en simulaciones simples de telas, cuerdas y cuerpos blandos. En lugar de trabajar explícitamente con velocidad, este método calcula la nueva posición de cada partícula a partir de su posición actual, su posición previa y las fuerzas aplicadas. Esto permite obtener un comportamiento estable y natural con una implementación relativamente sencilla.

Las conexiones entre puntos vecinos se modelan como **restricciones de distancia**. Cada una intenta conservar la longitud original entre dos nodos enlazados. En cada cuadro de animación, el script recorre varias veces estas restricciones y corrige las posiciones para evitar que la malla se estire demasiado. Gracias a este proceso iterativo, la estructura mantiene su coherencia sin necesidad de recurrir a una simulación física compleja basada en resortes clásicos.

Para lograr una apariencia más blanda y menos rígida, esta versión utiliza únicamente conexiones horizontales y verticales, evitando refuerzos diagonales. También se incorpora una ligera amortiguación en el movimiento, lo que reduce oscilaciones excesivas y contribuye a una caída más suave.

La interacción del usuario se organiza en dos ejes. Por un lado, se puede seleccionar uno de los cinco puntos de anclaje superiores mediante la tecla `TAB` y moverlo con las flechas del teclado. Por otro, se puede desgarrar la malla manteniendo presionado el botón izquierdo del mouse sobre la zona deseada. El script detecta qué conexiones pasan cerca del cursor y las elimina de la simulación.

En conjunto, el resultado es una pequeña demostración de física visual en tiempo real, útil tanto como experimento didáctico como base para proyectos más complejos relacionados con telas, redes, superficies deformables o efectos interactivos en 2D.

## Licencia

Este proyecto se distribuye bajo la licencia MIT. Consulte el archivo `LICENSE` para más información.

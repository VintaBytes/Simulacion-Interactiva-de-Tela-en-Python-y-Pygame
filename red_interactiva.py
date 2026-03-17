# ==========================================================
# IMPORTAR LIBRERIAS
# ==========================================================
import pygame
from pygame.math import Vector2

# ==========================================================
# CONFIGURACION GENERAL
# ==========================================================
ANCHO = 800
ALTO = 1000
FPS = 60

COLOR_FONDO = (20, 20, 28)
COLOR_LINEAS = (190, 210, 230)
COLOR_NODOS = (255, 220, 120)
COLOR_ANCLAJE = (255, 120, 120)
COLOR_TEXTO = (220, 220, 220)
COLOR_CURSOR_CORTE = (255, 80, 80)
COLOR_SELECCION = (120, 255, 120)

GRAVEDAD = Vector2(0, 0.55)
ITERACIONES_RESTRICCIONES = 5
AMORTIGUACION = 0.985

FILAS = 18
COLUMNAS = 28
ESPACIADO = 22

ORIGEN_X = 90
ORIGEN_Y = 80

RADIO_CORTE = 10


# ==========================================================
# CLASE PUNTO
# ==========================================================
class Punto:
    def __init__(self, x, y, fijo=False):
        self.posicion = Vector2(x, y)
        self.posicion_anterior = Vector2(x, y)
        self.aceleracion = Vector2(0, 0)
        self.fijo = fijo

    def aplicar_fuerza(self, fuerza):
        if not self.fijo:
            self.aceleracion += fuerza

    def actualizar(self):
        if self.fijo:
            self.aceleracion = Vector2(0, 0)
            return

        velocidad_aparente = (self.posicion - self.posicion_anterior) * AMORTIGUACION
        self.posicion_anterior = self.posicion.copy()
        self.posicion += velocidad_aparente + self.aceleracion
        self.aceleracion = Vector2(0, 0)

    def fijar_en(self, x, y):
        self.posicion.update(x, y)
        self.posicion_anterior.update(x, y)


# ==========================================================
# CLASE RESTRICCION
# ==========================================================
class Restriccion:
    def __init__(self, punto_a, punto_b):
        self.punto_a = punto_a
        self.punto_b = punto_b
        self.longitud = punto_a.posicion.distance_to(punto_b.posicion)

    def resolver(self):
        delta = self.punto_b.posicion - self.punto_a.posicion
        distancia = delta.length()

        if distancia == 0:
            return

        diferencia = (distancia - self.longitud) / distancia

        if self.punto_a.fijo and self.punto_b.fijo:
            return
        elif self.punto_a.fijo:
            self.punto_b.posicion -= delta * diferencia
        elif self.punto_b.fijo:
            self.punto_a.posicion += delta * diferencia
        else:
            correccion = delta * 0.5 * diferencia
            self.punto_a.posicion += correccion
            self.punto_b.posicion -= correccion


# ==========================================================
# FUNCIONES AUXILIARES
# ==========================================================
def obtener_columnas_fijas(columnas):
    return {
        0,
        columnas // 4,
        columnas // 2,
        (3 * columnas) // 4,
        columnas - 1
    }


# ==========================================================
def crear_malla(filas, columnas, espaciado, origen_x, origen_y):
    puntos = []
    restricciones = []

    columnas_fijas = obtener_columnas_fijas(columnas)

    for fila in range(filas):
        fila_puntos = []
        for columna in range(columnas):
            x = origen_x + columna * espaciado
            y = origen_y + fila * espaciado

            fijo = (fila == 0 and columna in columnas_fijas)
            punto = Punto(x, y, fijo=fijo)
            fila_puntos.append(punto)
        puntos.append(fila_puntos)

    # Solo horizontales y verticales para una tela mas blanda
    for fila in range(filas):
        for columna in range(columnas):
            if columna < columnas - 1:
                restricciones.append(Restriccion(puntos[fila][columna], puntos[fila][columna + 1]))
            if fila < filas - 1:
                restricciones.append(Restriccion(puntos[fila][columna], puntos[fila + 1][columna]))

    return puntos, restricciones


# ==========================================================
def obtener_anclajes_superiores(puntos):
    anclajes = []
    for punto in puntos[0]:
        if punto.fijo:
            anclajes.append(punto)
    return anclajes


# ==========================================================
def dibujar_malla(superficie, puntos, restricciones):
    for restriccion in restricciones:
        a = restriccion.punto_a.posicion
        b = restriccion.punto_b.posicion
        pygame.draw.line(superficie, COLOR_LINEAS, a, b, 1)

    for fila in puntos:
        for punto in fila:
            color = COLOR_ANCLAJE if punto.fijo else COLOR_NODOS
            radio = 5 if punto.fijo else 2
            pygame.draw.circle(
                superficie,
                color,
                (int(punto.posicion.x), int(punto.posicion.y)),
                radio
            )


# ==========================================================
def dibujar_texto(superficie, fuente, indice_anclaje):
    lineas = [
        "TAB/Flechas: mueven anclajes",
        "R: reiniciar    ESC: salir",
    ]

    y = 850
    for texto in lineas:
        imagen = fuente.render(texto, True, COLOR_TEXTO)
        superficie.blit(imagen, (12, y))
        y += 24


# ==========================================================
def distancia_punto_a_segmento(px, py, ax, ay, bx, by):
    abx = bx - ax
    aby = by - ay
    apx = px - ax
    apy = py - ay

    ab2 = abx * abx + aby * aby
    if ab2 == 0:
        dx = px - ax
        dy = py - ay
        return (dx * dx + dy * dy) ** 0.5

    t = (apx * abx + apy * aby) / ab2
    t = max(0, min(1, t))

    cx = ax + t * abx
    cy = ay + t * aby

    dx = px - cx
    dy = py - cy
    return (dx * dx + dy * dy) ** 0.5


# ==========================================================
def cortar_restricciones(restricciones, mouse_pos, radio_corte):
    mx, my = mouse_pos
    nuevas_restricciones = []

    for restriccion in restricciones:
        ax, ay = restriccion.punto_a.posicion
        bx, by = restriccion.punto_b.posicion

        distancia = distancia_punto_a_segmento(mx, my, ax, ay, bx, by)

        if distancia > radio_corte:
            nuevas_restricciones.append(restriccion)

    return nuevas_restricciones


def reiniciar_malla():
    return crear_malla(FILAS, COLUMNAS, ESPACIADO, ORIGEN_X, ORIGEN_Y)


# ==========================================================
# PROGRAMA PRINCIPAL
# ==========================================================
def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Tela blanda con desgarro y anclaje seleccionable")
    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont("consolas", 20)

    puntos, restricciones = reiniciar_malla()
    anclajes = obtener_anclajes_superiores(puntos)
    indice_anclaje = 0

    ejecutando = True
    while ejecutando:
        reloj.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False
                elif evento.key == pygame.K_r:
                    puntos, restricciones = reiniciar_malla()
                    anclajes = obtener_anclajes_superiores(puntos)
                    indice_anclaje = 0
                elif evento.key == pygame.K_TAB:
                    indice_anclaje = (indice_anclaje + 1) % len(anclajes)

        # --------------------------------------------------
        # Flechas: mover solo el anclaje seleccionado
        # --------------------------------------------------
        teclas = pygame.key.get_pressed()
        velocidad_anclaje = 3

        dx = 0
        dy = 0

        if teclas[pygame.K_LEFT]:
            dx -= velocidad_anclaje
        if teclas[pygame.K_RIGHT]:
            dx += velocidad_anclaje
        if teclas[pygame.K_UP]:
            dy -= velocidad_anclaje
        if teclas[pygame.K_DOWN]:
            dy += velocidad_anclaje

        if dx != 0 or dy != 0:
            anclaje_actual = anclajes[indice_anclaje]
            anclaje_actual.fijar_en(
                anclaje_actual.posicion.x + dx,
                anclaje_actual.posicion.y + dy
            )

        # --------------------------------------------------
        # Desgarro con mouse
        # --------------------------------------------------
        botones_mouse = pygame.mouse.get_pressed()
        posicion_mouse = pygame.mouse.get_pos()

        if botones_mouse[0]:
            restricciones = cortar_restricciones(
                restricciones,
                posicion_mouse,
                RADIO_CORTE
            )

        # --------------------------------------------------
        # Simulacion fisica
        # --------------------------------------------------
        for fila in puntos:
            for punto in fila:
                punto.aplicar_fuerza(GRAVEDAD)
                punto.actualizar()

        for _ in range(ITERACIONES_RESTRICCIONES):
            for restriccion in restricciones:
                restriccion.resolver()

        # --------------------------------------------------
        # Dibujo
        # --------------------------------------------------
        pantalla.fill(COLOR_FONDO)
        dibujar_malla(pantalla, puntos, restricciones)
        dibujar_texto(pantalla, fuente, indice_anclaje)

        # Resaltar anclaje seleccionado
        seleccionado = anclajes[indice_anclaje]
        pygame.draw.circle(
            pantalla,
            COLOR_SELECCION,
            (int(seleccionado.posicion.x), int(seleccionado.posicion.y)),
            9,
            2
        )

        # Dibujar indicador visual del area de corte
        if botones_mouse[0]:
            pygame.draw.circle(
                pantalla,
                COLOR_CURSOR_CORTE,
                posicion_mouse,
                RADIO_CORTE,
                2
            )

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
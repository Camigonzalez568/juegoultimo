import pygame, random, sys

pygame.init()
ANCHO, ALTO = 700, 500
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Alerta CO — Prevención del Monóxido de Carbono")
clock = pygame.time.Clock()

# --- COLORES Y FUENTES ---
FONDO = (220, 240, 255)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
font = pygame.font.SysFont("arial", 28)
boton_font = pygame.font.SysFont("arial", 26)

# --- IMÁGENES ---
jugador_img = pygame.transform.scale(pygame.image.load("imagenes/jugador.png"), (50, 50))
cocina_img = pygame.transform.scale(pygame.image.load("imagenes/estufa.png"), (80, 80))
ventilador_img = pygame.transform.scale(pygame.image.load("imagenes/ventilador.png"), (90, 90))
peligro_img = pygame.transform.scale(pygame.image.load("imagenes/peligro.png"), (40, 40))

# --- SONIDOS ---
pygame.mixer.music.load("sonidos/musica.mp3")
pygame.mixer.music.play(-1)
alarma = pygame.mixer.Sound("sonidos/alarma.mp3")
correcto = pygame.mixer.Sound("sonidos/correcto.mp3")

# --- VARIABLES ---
def reiniciar():
    global jugador, cocina, ventilador, riesgos, co_nivel, juego_terminado, gano, mensaje
    jugador = pygame.Rect(100, 250, 50, 50)
    cocina = pygame.Rect(550, 280, 80, 80)
    ventilador = pygame.Rect(550, 150, 90, 90)
    riesgos = [pygame.Rect(random.randint(100, 600), random.randint(80, 420), 40, 40) for _ in range(4)]
    co_nivel = 0
    juego_terminado = False
    gano = False
    mensaje = "Movete con las flechas y tocá la cocina para ventilar."

reiniciar()

# --- LOOP PRINCIPAL ---
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if e.type == pygame.MOUSEBUTTONDOWN and juego_terminado:
            if boton.collidepoint(e.pos):
                reiniciar()

    teclas = pygame.key.get_pressed()

    if not juego_terminado:
        # Movimiento
        if teclas[pygame.K_LEFT] and jugador.x > 0: jugador.x -= 5
        if teclas[pygame.K_RIGHT] and jugador.x < ANCHO - 50: jugador.x += 5
        if teclas[pygame.K_UP] and jugador.y > 0: jugador.y -= 5
        if teclas[pygame.K_DOWN] and jugador.y < ALTO - 50: jugador.y += 5

        # CO sube con el tiempo
        co_nivel += 0.05

        # Colisiones con riesgos
        for r in riesgos[:]:
            if jugador.colliderect(r):
                riesgos.remove(r)
                co_nivel += 5
                alarma.play()
                mensaje = "¡Cuidado! Hay una pérdida, ventilá rápido."

        # Si toca la cocina, se enciende el ventilador
        if jugador.colliderect(cocina):
            co_nivel -= 10
            if co_nivel < 0: co_nivel = 0
            correcto.play()
            mensaje = "¡Bien! Encendiste el ventilador y ventilaste el ambiente."

        # Fin del juego
        if co_nivel >= 100:
            juego_terminado = True
            alarma.play()
        if not riesgos and co_nivel < 50:
            gano = True
            juego_terminado = True

    # --- DIBUJAR ---
    pantalla.fill(FONDO)

    pantalla.blit(jugador_img, jugador)
    pantalla.blit(cocina_img, cocina)
    pantalla.blit(ventilador_img, ventilador)
    for r in riesgos:
        pantalla.blit(peligro_img, r)

    # Barra CO
    pygame.draw.rect(pantalla, (255, 0, 0), (50, 30, co_nivel * 5, 20))
    texto = font.render(f"Nivel CO: {int(co_nivel)}", True, NEGRO)
    pantalla.blit(texto, (50, 5))

    # Mensaje educativo
    if mensaje:
        m = font.render(mensaje, True, NEGRO)
        pantalla.blit(m, (ANCHO//2 - m.get_width()//2, 70))

    # Fin de juego
    if juego_terminado:
        if gano:
            msg = "¡Bien hecho! Ventilar previene la intoxicación"
            color = (0, 180, 0)
        else:
            msg = "¡Peligro! Intoxicación por monóxido de carbono"
            color = (255, 0, 0)
        t = font.render(msg, True, color)
        pantalla.blit(t, (ANCHO//2 - t.get_width()//2, ALTO//2 - 40))

        boton = pygame.Rect(ANCHO//2 - 70, ALTO//2 + 20, 140, 50)
        pygame.draw.rect(pantalla, NEGRO, boton, border_radius=8)
        txt_boton = boton_font.render("Reiniciar", True, BLANCO)
        pantalla.blit(txt_boton, (boton.centerx - txt_boton.get_width()//2, boton.centery - txt_boton.get_height()//2))

    pygame.display.flip()
    clock.tick(60)

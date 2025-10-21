import pygame, random, sys

pygame.init()
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Alerta CO — Versión simple")

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (200, 0, 0)
AZUL = (0, 100, 255)
VERDE = (0, 200, 0)
GRIS = (40, 40, 40)

fuente = pygame.font.Font(None, 36)

class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(AZUL)
        self.rect = self.image.get_rect(center=(100, ALTO//2))
        self.velocidad = 5
    def update(self, teclas):
        if teclas[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.velocidad
        if teclas[pygame.K_DOWN] and self.rect.bottom < ALTO:
            self.rect.y += self.velocidad
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT] and self.rect.right < ANCHO:
            self.rect.x += self.velocidad

class Estufa(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((70, 70))
        self.image.fill(ROJO)
        self.rect = self.image.get_rect(center=(random.randint(400, 750), random.randint(100, 500)))

class Ventana(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((70, 70))
        self.image.fill(VERDE)
        self.rect = self.image.get_rect(center=(random.randint(400, 750), random.randint(100, 500)))

todos = pygame.sprite.Group()
riesgos = pygame.sprite.Group()
ventanas = pygame.sprite.Group()

jugador = Jugador()
todos.add(jugador)

for _ in range(2):
    estufa = Estufa()
    riesgos.add(estufa)
    todos.add(estufa)

ventana = Ventana()
ventanas.add(ventana)
todos.add(ventana)

nivel_CO = 0
reloj = pygame.time.Clock()
jugando = True
mensaje = ""

while jugando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    teclas = pygame.key.get_pressed()
    jugador.update(teclas)

    if pygame.sprite.spritecollide(jugador, riesgos, False):
        nivel_CO += 0.3
        mensaje = "⚠️ ¡Peligro! Hay fuga de CO."
    else:
        nivel_CO -= 0.1
        nivel_CO = max(nivel_CO, 0)

    if pygame.sprite.spritecollide(jugador, ventanas, False):
        nivel_CO -= 2
        mensaje = "✅ ¡Bien! Ventilaste el ambiente."
    else:
        mensaje = mensaje if nivel_CO > 0 else "Ambiente seguro."

    if nivel_CO >= 100:
        mensaje = "💀 Te intoxicás con monóxido de carbono."
        jugando = False

    pantalla.fill(GRIS)
    todos.draw(pantalla)
    pygame.draw.rect(pantalla, ROJO, (50, 50, int(nivel_CO * 3), 20))
    pygame.draw.rect(pantalla, NEGRO, (50, 50, 300, 20), 2)
    texto = fuente.render(mensaje, True, BLANCO)
    pantalla.blit(texto, (50, 100))
    pygame.display.flip()
    reloj.tick(60)

pygame.time.wait(2500)
pygame.quit()

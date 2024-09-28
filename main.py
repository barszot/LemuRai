import pygame
import sys

# Inicjalizacja Pygame
pygame.init()

# Ustawienia okienka
szerokosc = 800
wysokosc = 600
ekran = pygame.display.set_mode((szerokosc, wysokosc))
pygame.display.set_caption('Moja gra w Pygame')

# Kolory
kolor_tla = (0, 0, 0)  # Czarny

# Główna pętla gry
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Rysowanie tła
    ekran.fill(kolor_tla)

    # Odświeżenie ekranu
    pygame.display.flip()

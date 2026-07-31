import pygame

def press_start(screen: pygame.Surface) -> None:
    """Displays a title screen and waits for any key press."""
    font = pygame.font.Font(None, 60)
    text = font.render("PRESS START", True, (255, 255, 0))
    text_rect = text.get_rect(center=(screen.get_width() // 2,
                                        screen.get_height() // 2))

    screen.fill((0, 0, 0))
    screen.blit(text, text_rect)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                waiting = False
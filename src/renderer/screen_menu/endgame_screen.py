import pygame
from ..display import NOIR, JAUNE

def display_endgame(screen: pygame.Surface, score: int = 0) -> bool:
    """Displays the endgame screen. Returns True if the player restarts."""
    font = pygame.font.Font(None, 60)
    font_small = pygame.font.Font(None, 30)
    centre_x = screen.get_width() // 2
    centre_y = screen.get_height() // 2

    screen.fill(NOIR)
    largeur, hauteur = 400, 200
    # draw_rect_pixel(screen, centre_x - largeur // 2,
    #                 centre_y - hauteur // 2, largeur, hauteur)

    text = font.render("GAME OVER", True, JAUNE)
    screen.blit(text, text.get_rect(center=(centre_x, centre_y - 45)))

    text_score = font_small.render(f"SCORE : {score}", True, JAUNE)
    screen.blit(text_score, text_score.get_rect(center=(centre_x, centre_y)))

    hint = font_small.render("ESPACE : REJOUER   -   ECHAP : QUITTER",
                             True, JAUNE)
    screen.blit(hint, hint.get_rect(center=(centre_x, centre_y + 50)))
    pygame.display.flip()

    pygame.event.clear()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                if event.key == pygame.K_ESCAPE:
                    return False
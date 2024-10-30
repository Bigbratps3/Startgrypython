import pygame
import time
import random
pygame.font.init()

Width, Height = 500, 700
pygame.init()
WIN = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Spadające gwiazdy")

sprite = pygame.transform.scale(pygame.image.load("Poziom.png"), (Width, Height))

PLAYER_Width = 40
PLAYER_Height = 60
PLAYER_VEL = 5
STAR_Width = 10
STAR_Height = 20
STAR_VEL = 10

FONT = pygame.font.SysFont("comicsans", 30)

def draw(player, elapsed_time, stars):
    WIN.blit(sprite, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "purple")
    text_width, text_height = FONT.size(f"Time: {round(elapsed_time)}s")
    text_x = (Width - text_width) // 2
    
    WIN.blit(time_text, (text_x, 10))

    pygame.draw.rect(WIN, "blue", player)

    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    pygame.display.update()

def main():
    run = True

    player = pygame.Rect(300, Height - PLAYER_Height,
                          PLAYER_Width, PLAYER_Height)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0

    stars = []
    hit = False

    while run:
        star_count += clock.tick(100)
        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
            star_x = random.randint(0, Width - STAR_Width)
            star = pygame.Rect(star_x, -STAR_Height,
                                STAR_Width, STAR_Height)
            stars.append(star)

            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               run = False
               break

        # Movement keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - PLAYER_VEL >= 0:
                player.x -= PLAYER_VEL
        if keys[pygame.K_d] and player.x + PLAYER_VEL + PLAYER_Width <= Width:
                player.x += PLAYER_VEL
        if keys[pygame.K_w] and player.y - PLAYER_VEL >= 0:
                player.y -= PLAYER_VEL
        if keys[pygame.K_s] and player.y + PLAYER_VEL + PLAYER_Height <= Height:
                player.y += PLAYER_VEL
        
        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > Height:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        if hit:
            lost_text = FONT.render("YOU LOSE!", 1, "red" )
            WIN.blit(lost_text, (Width/2 - lost_text.get_width()/2, Height/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break
            
        draw(player, elapsed_time, stars)

def main_menu():
    run = True
    while run:
        WIN.blit(sprite, (0, 0))
        
        title_text = FONT.render("Spadające Gwiazdy", 1, "white")
        start_text = FONT.render("Press ENTER to Start", 1, "yellow")
        quit_text = FONT.render("Press Q to Quit", 1, "yellow")

        WIN.blit(title_text, (Width/2 - title_text.get_width()/2, Height/2 - title_text.get_height() - 20))
        WIN.blit(start_text, (Width/2 - start_text.get_width()/2, Height/2 + 10))
        WIN.blit(quit_text, (Width/2 - quit_text.get_width()/2, Height/2 + 40))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main()  # Start the game
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

if __name__ == "__main__":
    main_menu()

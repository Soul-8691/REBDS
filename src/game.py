import json
import random
import pygame
import os

def game_loop(root):
    # Initialize Pygame
    pygame.init()

    # Set up the display
    screen_width, screen_height = 1000, 750
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Yu-Gi-Oh! Duel')

    # Initialize Pygame
    pygame.init()

    # Load the main deck
    with open('src/decks/main_deck.json', 'r') as file:
        main_deck = json.load(file)

    # Randomly select 5 cards for the player's hand
    player_hand = random.sample(sorted(main_deck), 5)

    # Load card images
    image_folder = '../YGO Card Images/'
    card_images = {root.items[card_name]: pygame.transform.scale(pygame.image.load(os.path.join(image_folder, f'{root.items[card_name]}.jpg')), (150, 218)) for card_name in player_hand}

    # Load card back image
    card_back_image = pygame.transform.scale(pygame.image.load(os.path.join(image_folder, 'card_back.png')), (150, 218))
    root.backs = False

    def slide_in_card(image, start_pos, end_pos, duration, drawn_cards, drawn_cards_backs):
        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()

        while True:
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - start_time

            if elapsed_time > duration:
                break
            
            t = elapsed_time / duration
            current_pos = (start_pos[0] + t * (end_pos[0] - start_pos[0]),
                        start_pos[1] + t * (end_pos[1] - start_pos[1]))

            # Clear screen
            screen.fill((0, 0, 0))

            # Redraw all previously drawn cards
            for card, pos in drawn_cards:
                screen.blit(card, pos)
            # Redraw all previously drawn cards
            for card, pos in drawn_cards_backs:
                screen.blit(card, pos)

            # Draw the current card
            screen.blit(image, current_pos)
            pygame.display.flip()
            clock.tick(60)

        # Add the final position of the current card to the drawn list
        if root.backs == False:
            drawn_cards.append((image, end_pos))
        else:
            drawn_cards_backs.append((image, end_pos))

    # Define positions
    y_position = screen_height - 200  # Position near the bottom

    # Slide in each card
    drawn_cards = []  # Keep track of drawn cards
    drawn_cards_backs = []

    for i, card_name in enumerate(player_hand):
        start_pos = (-100, y_position)
        end_pos = (50 + i * 150, y_position)
        slide_in_card(card_images[root.items[card_name]], start_pos, end_pos, 500, drawn_cards, drawn_cards_backs)
    
    root.backs = True

    # Define positions
    opponent_x_positions = [50 + i * 150 for i in range(5)]
    opponent_y_position = 50  # Position near the top

    # Blit card backs
    for x in opponent_x_positions:
        start_pos = (-100, opponent_y_position)
        end_pos = (x, opponent_y_position)
        slide_in_card(card_back_image, start_pos, end_pos, 500, drawn_cards, drawn_cards_backs)
    pygame.display.flip()

    # Initialize font
    pygame.font.init()
    font = pygame.font.SysFont(None, 55)

    # Render text
    text = font.render('Duel started: The duel is ready to begin.', True, (255, 255, 255))

    # Blit text to screen
    screen.blit(text, (50, screen_height // 2 - 50))
    pygame.display.flip()

    # Wait for a short duration
    pygame.time.wait(2000)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.time.wait(100)
    pygame.quit()

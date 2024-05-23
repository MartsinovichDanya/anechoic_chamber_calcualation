import pygame
import sys
import math
import random
import time

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 1000, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Billiards")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Ball properties
BALL_RADIUS = 10

balls = []  # List to store information about each ball
font = pygame.font.Font(None, 24)

# Main loop
running = True
last_ball_time = 0  

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
              running = False

    if time.time() - last_ball_time >= 3:  # Launch a ball every 2 seconds
        ball = {
            "x": -400 + WIDTH // 2,  
            "y": HEIGHT // 2,  
            "speed": 20,
            "angle": math.radians(random.uniform(-45, 45)),
            "collision_count": 0,
            "started": False,
            "launch_time": time.time(),
            "info_text": None,
            "show_info_time": None,
            "ball_number": len(balls) + 1  # Unique number for each ball
           
            
        }
        balls.append(ball)
        last_ball_time = time.time()
  
               

    for ball in balls:
        if not ball["started"]:
            ball["started"] = True
            ball["collision_count"] = 0  # Reset collision count for the new ball
           
        else:
            ball["x"] += ball["speed"] * math.cos(ball["angle"])
            ball["y"] += ball["speed"] * math.sin(ball["angle"])

            if ball["x"] <= BALL_RADIUS:
                ball["angle"] = math.pi - ball["angle"]
            if ball["y"] <= BALL_RADIUS or ball["y"] >= HEIGHT - BALL_RADIUS:
                ball["angle"] = -ball["angle"]
                ball["collision_count"] += 1
                
            if ball["x"] >= WIDTH:
                #ball["ball_number"] += 1
                balls.remove(ball)
               

        screen.fill(WHITE)
        pygame.draw.circle(screen, RED, (int(ball["x"]), int(ball["y"])), BALL_RADIUS)

        info_text = f"Collisions: {ball['collision_count']}"
        collision_text = font.render(info_text, True, BLACK)
        screen.blit(collision_text, (140,  20))
     
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()

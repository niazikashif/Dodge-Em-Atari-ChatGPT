import pygame
import sys
import random
import logging

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge 'Em")

# Clock for controlling the frame rate
CLOCK = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# Track dimensions
LANE_WIDTH = 50
NUM_LANES = 4

# Car dimensions
CAR_SIZE = 20

# Gap size for lane switching
GAP_SIZE = 80

# Fonts
FONT = pygame.font.SysFont(None, 36)

# Player speed variables
SPEED_NORMAL = 2
SPEED_BOOST = 4

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(message)s')


# Define the Car class
class Car:
    def __init__(self, lane, color, speed, direction='right'):
        self.lane = lane  # Current lane (0 = outermost)
        self.color = color
        self.speed = speed
        self.direction = direction  # Current moving direction
        self.update_lane_parameters()
        self.position = self.get_start_position()
        self.turn_requested = None  # No turn requested initially

    def update_lane_parameters(self):
        # Update parameters based on current lane
        lane_offset = LANE_WIDTH * self.lane + LANE_WIDTH / 2
        self.left = lane_offset
        self.top = lane_offset
        self.right = WIDTH - lane_offset - CAR_SIZE
        self.bottom = HEIGHT - lane_offset - CAR_SIZE
        logging.debug(f"Lane parameters updated: Lane {self.lane}, Left {self.left}, Top {self.top}, Right {self.right}, Bottom {self.bottom}")

    def get_start_position(self):
        if self.direction == 'right':
            # Start at left edge, y at center
            y_center = (self.top + self.bottom) / 2
            return [self.left, y_center]
        elif self.direction == 'left':
            # Start at right edge, y at center
            y_center = (self.top + self.bottom) / 2
            return [self.right, y_center]
        elif self.direction == 'down':
            # Start at top edge, x at center
            x_center = (self.left + self.right) / 2
            return [x_center, self.top]
        elif self.direction == 'up':
            # Start at bottom edge, x at center
            x_center = (self.left + self.right) / 2
            return [x_center, self.bottom]

    def move(self):
        x, y = self.position

        if self.direction == 'right':
            x += self.speed
            if x >= self.right:
                x = self.right
                self.at_corner()
        elif self.direction == 'down':
            y += self.speed
            if y >= self.bottom:
                y = self.bottom
                self.at_corner()
        elif self.direction == 'left':
            x -= self.speed
            if x <= self.left:
                x = self.left
                self.at_corner()
        elif self.direction == 'up':
            y -= self.speed
            if y <= self.top:
                y = self.top
                self.at_corner()
        self.position = [x, y]
        logging.debug(f"Car moved to position {self.position}, direction {self.direction}")

        # Check if a turn is requested at a gap
        if self.turn_requested and self.at_gap():
            logging.debug(f"Turn requested ({self.turn_requested}) at gap.")
            self.change_lane_and_direction(self.turn_requested)
            self.turn_requested = None

    def at_corner(self):
        if self.turn_requested:
            logging.debug(f"Turn requested ({self.turn_requested}) at corner.")
            self.change_direction(self.turn_requested)
            self.turn_requested = None
        else:
            logging.debug(f"No turn requested at corner. Turning right by default.")
            self.turn_right()

    def change_direction(self, turn):
        if turn == 'left':
            self.turn_left()
        elif turn == 'right':
            self.turn_right()
        logging.debug(f"Changed direction to {self.direction}")
        
    def change_lane(self, turn):
        logging.debug(f"Changing lane: turn {turn}, current lane {self.lane}, direction {self.direction}")
        previous_lane = self.lane  # Keep track of the previous lane

        if turn == 'left':
            # Move inward if possible
            if self.lane < NUM_LANES - 1:
                self.lane += 1
                logging.debug(f"Moved inward to lane {self.lane}")
            else:
                logging.debug("Already at innermost lane; cannot move inward.")
        elif turn == 'right':
            # Move outward if possible
            if self.lane > 0:
                self.lane -= 1
                logging.debug(f"Moved outward to lane {self.lane}")
            else:
                logging.debug("Already at outermost lane; cannot move outward.")

        # Ensure lane number stays within bounds
        self.lane = max(0, min(self.lane, NUM_LANES - 1))

        # Update lane parameters
        self.update_lane_parameters()

        # Adjust position to be within new lane boundaries
        if self.direction in ['left', 'right']:
            # For horizontal movement, adjust y to center of new lane
            self.position[1] = (self.top + self.bottom) / 2
        elif self.direction in ['up', 'down']:
            # For vertical movement, adjust x to center of new lane
            self.position[0] = (self.left + self.right) / 2

        logging.debug(f"Position adjusted after lane change: {self.position}, direction {self.direction}, lane changed from {previous_lane} to {self.lane}")


    def change_lane_and_direction(self, turn):
        logging.debug(f"Changing lane and direction: turn {turn}, current lane {self.lane}, direction {self.direction}")
        previous_lane = self.lane  # Keep track of the previous lane

        if turn == 'left':
            # Move inward if possible
            if self.lane < NUM_LANES - 1:
                self.lane += 1
                logging.debug(f"Moved inward to lane {self.lane}")
            else:
                logging.debug("Already at innermost lane; cannot move inward.")
        elif turn == 'right':
            # Move outward if possible
            if self.lane > 0:
                self.lane -= 1
                logging.debug(f"Moved outward to lane {self.lane}")
            else:
                logging.debug("Already at outermost lane; cannot move outward.")

        # Ensure lane number stays within bounds
        self.lane = max(0, min(self.lane, NUM_LANES - 1))

        # Update lane parameters
        self.update_lane_parameters()

        # Change direction appropriately
        self.change_direction(turn)

        # Adjust position to be within new lane boundaries based on new direction
        if self.direction == 'right':
            self.position[0] = self.left
            self.position[1] = (self.top + self.bottom) / 2
        elif self.direction == 'left':
            self.position[0] = self.right
            self.position[1] = (self.top + self.bottom) / 2
        elif self.direction == 'down':
            self.position[0] = (self.left + self.right) / 2
            self.position[1] = self.top
        elif self.direction == 'up':
            self.position[0] = (self.left + self.right) / 2
            self.position[1] = self.bottom

        logging.debug(f"Position adjusted after lane change: {self.position}, direction {self.direction}, lane changed from {previous_lane} to {self.lane}")



    def turn_left(self):
        # Change direction to the left (counter-clockwise)
        directions = ['up', 'left', 'down', 'right']
        idx = directions.index(self.direction)
        self.direction = directions[(idx - 1) % 4]
        logging.debug(f"Turned left. New direction: {self.direction}")

    def turn_right(self):
        # Change direction to the right (clockwise)
        directions = ['up', 'right', 'down', 'left']
        idx = directions.index(self.direction)
        self.direction = directions[(idx + 1) % 4]
        logging.debug(f"Turned right. New direction: {self.direction}")

    def request_turn(self, turn):
        self.turn_requested = turn
        logging.debug(f"Turn requested: {turn}")

    def at_gap(self):
        x, y = self.position

        if self.direction in ['up', 'down']:
            # For vertical movement, check y-coordinate
            gap_y_start = self.top + (self.bottom - self.top + CAR_SIZE - GAP_SIZE) / 2
            gap_y_end = gap_y_start + GAP_SIZE
            at_gap = gap_y_start <= y <= gap_y_end
            logging.debug(f"At_gap vertical check (Car color: {self.color}): y={y}, gap_y_start={gap_y_start}, gap_y_end={gap_y_end}, at_gap={at_gap}")
            return at_gap
        elif self.direction in ['left', 'right']:
            # For horizontal movement, check x-coordinate
            gap_x_start = self.left + (self.right - self.left + CAR_SIZE - GAP_SIZE) / 2
            gap_x_end = gap_x_start + GAP_SIZE
            at_gap = gap_x_start <= x <= gap_x_end
            logging.debug(f"At_gap horizontal check (Car color: {self.color}): x={x}, gap_x_start={gap_x_start}, gap_x_end={gap_x_end}, at_gap={at_gap}")
            return at_gap
        return False

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (*self.position, CAR_SIZE, CAR_SIZE))


# The rest of the code remains the same, including the create_dots function and the main game loop.

# Function to create dots
def create_dots():
    dots = []
    for lane in range(NUM_LANES):
        lane_offset = LANE_WIDTH * lane + LANE_WIDTH / 2
        left = lane_offset
        top = lane_offset
        right = WIDTH - lane_offset - CAR_SIZE
        bottom = HEIGHT - lane_offset - CAR_SIZE

        # Top and bottom edges
        for x in range(int(left + CAR_SIZE), int(right), 20):
            if abs(x - (left + right) / 2) > GAP_SIZE / 2:
                dots.append(pygame.Rect(x, top, 6, 6))
                dots.append(pygame.Rect(x, bottom, 6, 6))

        # Left and right edges
        for y in range(int(top + CAR_SIZE), int(bottom), 20):
            if abs(y - (top + bottom) / 2) > GAP_SIZE / 2:
                dots.append(pygame.Rect(left, y, 6, 6))
                dots.append(pygame.Rect(right, y, 6, 6))
    return dots

# Main game function
def main():
    # Initialize player and AI cars
    player = Car(0, BLUE, SPEED_NORMAL, direction='right')  # Outermost lane
    ai_car = Car(NUM_LANES - 1, RED, SPEED_NORMAL + 1, direction='left')  # Innermost lane

    # Dots
    dots = create_dots()

    # Game variables
    score = 0
    lives = 3
    level = 1
    running = True

    # AI behavior variables
    ai_chasing = False  # AI starts without chasing the player
    laps_before_chase = 1
    ai_lap_count = 0
    ai_start_position = ai_car.position[:]

    while running:
        CLOCK.tick(FPS)
        SCREEN.fill(GRAY)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Handle player input for turning
                if event.key == pygame.K_LEFT:
                    if player.at_gap():
                        logging.debug("Left key pressed at gap")
                        player.request_turn('left')
                    else:
                        logging.debug("Left key pressed, but not at gap")
                elif event.key == pygame.K_RIGHT:
                    if player.at_gap():
                        logging.debug("Right key pressed at gap")
                        player.request_turn('right')
                    else:
                        logging.debug("Right key pressed, but not at gap")
                elif event.key == pygame.K_SPACE:
                    player.speed = SPEED_BOOST
                    logging.debug("Speed boost activated")
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    player.speed = SPEED_NORMAL
                    logging.debug("Speed boost deactivated")

        # Move cars
        player.move()
        ai_car.move()

        # AI car behavior
        if ai_car.at_gap():
            if ai_chasing:
                # Simple chasing logic: attempt to get into the same lane as the player
                if ai_car.lane > player.lane:
                    ai_car.request_turn('right')  # Move outward
                elif ai_car.lane < player.lane:
                    ai_car.request_turn('left')  # Move inward
                else:
                    pass  # Same lane, continue movement
            else:
                ai_car.turn_right()  # Default movement
                # Check if AI completed a lap
                if ai_car.direction == 'left' and distance(ai_car.position, ai_start_position) < 5:
                    ai_lap_count += 1
                    if ai_lap_count >= laps_before_chase:
                        ai_chasing = True

        # Collision detection
        player_rect = pygame.Rect(*player.position, CAR_SIZE, CAR_SIZE)
        ai_rect = pygame.Rect(*ai_car.position, CAR_SIZE, CAR_SIZE)
        if player_rect.colliderect(ai_rect):
            lives -= 1
            logging.debug(f"Collision detected! Lives remaining: {lives}")
            if lives <= 0:
                # Game over
                running = False
            else:
                # Reset positions
                player = Car(0, BLUE, SPEED_NORMAL, direction='right')
                ai_car = Car(NUM_LANES - 1, RED, SPEED_NORMAL + level, direction='left')
                ai_chasing = False
                ai_lap_count = 0
                ai_start_position = ai_car.position[:]

        # Collect dots
        for dot in dots[:]:
            if player_rect.colliderect(dot):
                dots.remove(dot)
                score += 10
                logging.debug(f"Dot collected! Score: {score}")

        # Level progression
        if not dots:
            level += 1
            ai_car.speed += 0.5  # Increase AI car speed
            dots = create_dots()
            # Reset AI behavior
            ai_chasing = False
            ai_lap_count = 0
            ai_start_position = ai_car.position[:]
            logging.debug(f"Level up! Now at level {level}")

        # Draw track
        for lane in range(NUM_LANES):
            lane_offset = LANE_WIDTH * lane + LANE_WIDTH / 2
            rect = pygame.Rect(
                lane_offset,
                lane_offset,
                WIDTH - 2 * lane_offset,
                HEIGHT - 2 * lane_offset
            )
            pygame.draw.rect(SCREEN, WHITE, rect, 2)
            # Draw gaps (allowing turning)
            gap_positions = [
                (rect.left + (rect.width - GAP_SIZE) / 2, rect.top - 1, GAP_SIZE, 3),
                (rect.left + (rect.width - GAP_SIZE) / 2, rect.bottom - 2, GAP_SIZE, 3),
                (rect.left - 1, rect.top + (rect.height - GAP_SIZE) / 2, 3, GAP_SIZE),
                (rect.right - 2, rect.top + (rect.height - GAP_SIZE) / 2, 3, GAP_SIZE)
            ]
            for gap_rect in gap_positions:
                pygame.draw.rect(SCREEN, GRAY, gap_rect)

        # Draw dots
        for dot in dots:
            pygame.draw.rect(SCREEN, YELLOW, dot)

        # Draw cars
        player.draw(SCREEN)
        ai_car.draw(SCREEN)

        # Display score and lives
        score_text = FONT.render(f"Score: {score}", True, WHITE)
        lives_text = FONT.render(f"Lives: {lives}", True, WHITE)
        level_text = FONT.render(f"Level: {level}", True, WHITE)
        SCREEN.blit(score_text, (10, 10))
        SCREEN.blit(lives_text, (10, 50))
        SCREEN.blit(level_text, (10, 90))

        pygame.display.flip()

    # Game over screen
    SCREEN.fill(BLACK)
    game_over_text = FONT.render("Game Over", True, WHITE)
    final_score_text = FONT.render(f"Final Score: {score}", True, WHITE)
    SCREEN.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
    SCREEN.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

# Function to calculate distance between two positions
def distance(pos1, pos2):
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5

if __name__ == "__main__":
    main()

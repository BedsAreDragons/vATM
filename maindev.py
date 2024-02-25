import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = pygame.display.get_surface().get_size()
pygame.display.set_caption("Aircraft Above London")

# London boundaries
london_bounds = {'min_latitude': 49.718658, 'max_latitude': 53.967848, 'min_longitude': -6.206157, 'max_longitude': 1.965272}

# Aircraft data
aircraft_list = [
    {'callsign': 'ABC123', 'latitude': 51.5, 'longitude': 0.5, 'altitude': 30000, 'heading': 150, 'speed': 500,
     'departure': 'JFK', 'arrival': 'LHR', 'flight_plan': 'DIRECT', 'cruise_altitude': 35000, 'squawk': '1234'},
    {'callsign': 'XYZ789', 'latitude': 53.0, 'longitude': 0.8, 'altitude': 35000, 'heading': 270, 'speed': 600,
     'departure': 'LHR', 'arrival': 'JFK', 'flight_plan': 'VIA UL9', 'cruise_altitude': 37000, 'squawk': '5678'},
]

# Function to convert coordinates to screen position
def convert_to_screen(latitude, longitude):
    x = int((longitude - london_bounds['min_longitude']) / (london_bounds['max_longitude'] - london_bounds['min_longitude']) * screen_width)
    y = int((latitude - london_bounds['min_latitude']) / (london_bounds['max_latitude'] - london_bounds['min_latitude']) * screen_height)
    return x, y

# Function to display aircraft on the screen
def display_aircraft(screen, aircraft_list):
    screen.fill((0, 0, 0))  # Clear the screen

    # Draw radar scope circles in the middle
    center_x, center_y = screen_width // 2, screen_height // 2
    pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), 50, 2)
    pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), 100, 2)
    pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), 150, 2)
    pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), 200, 2)
    pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), 250, 2)

    font = pygame.font.Font(None, 24)

    for aircraft in aircraft_list:
        # Convert coordinates to screen position
        screen_x, screen_y = convert_to_screen(aircraft['latitude'], aircraft['longitude'])

        # Draw the square at the aircraft's position
        pygame.draw.rect(screen, (255, 255, 255), (screen_x - 10, screen_y - 10, 20, 20))

        # Draw the corrected heading line
        rad_heading = math.radians(aircraft['heading'] - 90)  # Adjusting to start from the top (North)
        line_length = 30
        end_pos = (screen_x + int(line_length * math.cos(rad_heading)),
                   screen_y + int(line_length * math.sin(rad_heading)))
        pygame.draw.line(screen, (255, 255, 255), (screen_x, screen_y), end_pos, 2)

        # Display additional information
        info_text = f"{aircraft['callsign']}  {aircraft['altitude']}"
        text_render = font.render(info_text, True, (255, 255, 255))
        text_rect = text_render.get_rect(midtop=(screen_x + 70, screen_y + 15))  # Adjusted position
        screen.blit(text_render, text_rect)

    pygame.display.flip()  # Update the display

# Function to display detailed information about an aircraft in a new window
def display_aircraft_info(aircraft):
    font = pygame.font.Font(None, 24)

    info_screen = pygame.display.set_mode((1200, 600), pygame.FULLSCREEN)
    pygame.display.set_caption(f"Aircraft Info - {aircraft['callsign']}")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # Display detailed information
        info_text = (
            f"Departure: {aircraft['departure']}\n"
            f"Arrival: {aircraft['arrival']}\n"
            f"Flight Plan: {aircraft['flight_plan']}\n"
            f"Cruise Altitude: {aircraft['cruise_altitude']}\n"
            f"Current Altitude: {aircraft['altitude']}\n"
            f"Current Heading: {aircraft['heading']}\n"
            f"Speed: {aircraft['speed']}\n"
            f"Squawk: {aircraft['squawk']}"
        )
        text_render = font.render(info_text, True, (255, 255, 255))
        text_rect = text_render.get_rect(topleft=(20, 20))
        info_screen.blit(text_render, text_rect)
        pygame.display.flip()

    # Do not quit Pygame and exit here to keep the main window open

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse click is on an aircraft
            for aircraft in aircraft_list:
                screen_x, screen_y = convert_to_screen(aircraft['latitude'], aircraft['longitude'])
                if screen_x - 10 <= event.pos[0] <= screen_x + 10 and screen_y - 10 <= event.pos[1] <= screen_y + 10:
                    # Display detailed information in a new window
                    display_aircraft_info(aircraft)

    # Display the aircraft on the screen
    display_aircraft(screen, aircraft_list)

    # Simulate real-time updates by waiting for a short duration
    pygame.time.delay(10)

# Quit Pygame and exit
pygame.quit()
sys.exit()

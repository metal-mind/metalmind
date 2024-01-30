""" Very simple interactive demo of two neurons stimulating a third. Has simple stimulation, decay, and refractory period dynamics. Note: don't attempt to derive insight into neural mechanics
through examining this code base, rather this is meant as an interactive demo to create a better understanding of the dynamics.
"""

import time
import pygame
import math

# Constants
WIDTH, HEIGHT = 842, 482
NEURON_RADIUS = 60
NEURON_COLOR = (0, 0, 0)
NEURON_ACTIVE_COLOR = (255, 0, 0)  # Color when neuron is clicked
LINE_COLOR = (100, 100, 100)
ACTIVE_DURATION = 0.4  # Duration for active color in seconds


NEURON1_POS = (121, 151)
NEURON2_POS = (121, 331)
OUTPUT_NEURON_POS = (701, 241)

# Track neuron activation
neuron_activation = {
    'neuron1': False,
    'neuron2': False,
    'output': False
}
activation_times = {
    'neuron1': 0,
    'neuron2': 0,
    'output': 0
}


# Stimulation bar properties
stimulation_bar_position = (803, 0)
stimulation_bar_size = (400, 480)
stimulation_bar_color = (0, 128, 0)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.image.load("./2-input-neuron.png")


def draw_neuron(pos, active=False):
    if active:
        pygame.draw.circle(screen, NEURON_ACTIVE_COLOR, pos, NEURON_RADIUS)

    else:
        pygame.draw.circle(screen, NEURON_COLOR, pos, NEURON_RADIUS, width=2)


def draw_connection(start_pos, end_pos):
    # Calculate angle
    dx = end_pos[0] - start_pos[0]
    dy = end_pos[1] - start_pos[1]
    angle = math.atan2(dy, dx)

    # Calculate new start and end points
    start_x = int(start_pos[0] + NEURON_RADIUS * math.cos(angle))
    start_y = int(start_pos[1] + NEURON_RADIUS * math.sin(angle))
    end_x = int(end_pos[0] - NEURON_RADIUS * math.cos(angle))
    end_y = int(end_pos[1] - NEURON_RADIUS * math.sin(angle))

    pygame.draw.line(screen, LINE_COLOR, (start_x, start_y), (end_x, end_y), 2)


def is_within_radius(point, circle_center, radius):
    x, y = point
    center_x, center_y = circle_center
    return (x - center_x) ** 2 + (y - center_y) ** 2 <= radius ** 2


def draw_active_neuron(neuron):
    neuron_activation[neuron] = True
    activation_times[neuron] = time.time()


def draw_inactive_neuron(neuron):
    neuron_activation[neuron] = False


# Function to draw the stimulation bar
def draw_stimulation_bar(percentage):
    # Calculate the current height of the stimulation bar based on the percentage
    current_height = int(stimulation_bar_size[1] * percentage / 100)

    # Calculate the top y position of the stimulation bar
    y_position = stimulation_bar_position[1] + (stimulation_bar_size[1] - current_height)

    # Clear the stimulation bar area
    pygame.draw.rect(screen, NEURON_COLOR, (stimulation_bar_position, stimulation_bar_size))

    # Draw the updated stimulation bar
    stimulation_bar_rect = pygame.Rect(stimulation_bar_position[0], y_position, stimulation_bar_size[0], current_height)
    pygame.draw.rect(screen, stimulation_bar_color, stimulation_bar_rect)



def main():

    input_to_output_stimulations = 60.0
    output_stimulation_level = 0.0
    output_activation_level = 100.0
    decay_rate = 0.15
    refractory_period = 1.5

    pygame.display.set_caption("Neuron Simulation")

    running = True
    while running:
        # screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        current_time = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if is_within_radius(mouse_pos, NEURON1_POS, NEURON_RADIUS):
                    # print("Input Neuron 1 clicked")
                    if current_time - activation_times["neuron1"] > refractory_period:  # Check refractory period and limit activation speed
                        output_stimulation_level += input_to_output_stimulations
                        draw_active_neuron('neuron1')
                elif is_within_radius(mouse_pos, NEURON2_POS, NEURON_RADIUS):
                    # print("Input Neuron 2 clicked")
                    if current_time - activation_times["neuron2"] > refractory_period:  # Check refractory period and limit activation speed
                        output_stimulation_level += input_to_output_stimulations
                    draw_active_neuron('neuron2')

        # Check output activation
        if output_stimulation_level > output_activation_level:
            draw_active_neuron('output')
            output_stimulation_level = output_activation_level
        elif output_stimulation_level > 0.0 and \
            output_stimulation_level != output_activation_level:  # Don't decay a full activation to make it clear that the neuron is firing
            output_stimulation_level -= decay_rate
        elif output_stimulation_level < 0.0:
            output_stimulation_level = 0.0
        # Draw neurons with activation check
        draw_neuron(NEURON1_POS, neuron_activation['neuron1'])
        draw_neuron(NEURON2_POS, neuron_activation['neuron2'])
        draw_neuron(OUTPUT_NEURON_POS, neuron_activation['output'])
        draw_stimulation_bar(output_stimulation_level)

        # Deactivate neurons after ACTIVE_DURATION
        for neuron in neuron_activation:
            if neuron_activation[neuron] and current_time - activation_times[neuron] > ACTIVE_DURATION:
                draw_inactive_neuron(neuron)
                if neuron == "output":
                    output_stimulation_level = 0.0

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()

# Utility function for one-arc collision logic
import numpy as np
import math
import pygame
import os
import imageio
import numpy as np
import random
from datetime import datetime
import math

def check_ring_collision(ball_pos, ball_velocity, center, radius, thickness, gap_start, gap_size, ball_radius):
    """
    Checks for collision between a ball and a single arc ring (with a rotating gap).
    If collision occurs outside the gap and within the ring's thickness, reflects the ball's velocity.

    Parameters:
        ball_pos (np.array): Ball position (x, y)
        ball_velocity (np.array): Ball velocity (x, y)
        center (np.array): Center of the arc ring (x, y)
        radius (float): Radius of the arc ring
        thickness (float): Ring's thickness
        gap_start (float): Starting angle of the gap (in radians)
        gap_size (float): Angular size of the gap (in radians)
        ball_radius (float): Radius of the ball

    Returns:
        np.array: Updated velocity vector (x, y)
    """
    dir = ball_pos - center
    dist = np.linalg.norm(dir)
    angle = math.atan2(dir[1], dir[0]) % (2 * math.pi)

    inner = radius - thickness / 2
    outer = radius + thickness / 2

    radial_hit = inner <= dist + ball_radius <= outer

    gap_end = (gap_start + gap_size) % (2 * math.pi)
    if gap_start < gap_end:
        in_gap = gap_start <= angle <= gap_end
    else:
        in_gap = angle >= gap_start or angle <= gap_end

    if radial_hit and not in_gap:
        if dist != 0:
            normal = dir / dist
            ball_velocity -= 2 * np.dot(ball_velocity, normal) * normal
            ball_velocity *= 0.95  # damping
    return ball_velocity

# Constants
radius = 200
thickness = 10
current_angle = 0
gap_size = math.radians(45)
gap_start = current_angle % (2 * math.pi)  # rotating over time
gap_end = (gap_start + gap_size) % (2 * math.pi)

# Physics
gravity = np.array([0, 0.05])
ball_velocity = np.array([0, 0.05])
ball_pos = np.array([0, 0.0])
ball_radius = 0.1
center = np.array([0, 0.0])
ball_velocity += gravity
ball_pos += ball_velocity

# Ball-to-center vector
dir = ball_pos - center
dist = np.linalg.norm(dir)
angle = math.atan2(dir[1], dir[0]) % (2 * math.pi)

# Arc thickness collision window
inner = radius - thickness / 2
outer = radius + thickness / 2

# Check radial + angular overlap
radial_hit = inner <= dist + ball_radius <= outer

# Handle gap wrapping 0 rad
if gap_start < gap_end:
    in_gap = gap_start <= angle <= gap_end
else:
    in_gap = angle >= gap_start or angle <= gap_end

# If collided with arc wall and not in the gap
if radial_hit and not in_gap:
    normal = dir / dist if dist != 0 else np.array([0, 0])
    ball_velocity -= 2 * np.dot(ball_velocity, normal) * normal
    ball_velocity *= 0.95  # optional damping

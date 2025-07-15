import pygame
import os
import imageio
import numpy as np
import random
from datetime import datetime
import math
from one_arc import check_ring_collision

# --- Config ---
WIDTH, HEIGHT = 720, 720
FPS = 30
DURATION = 20
FRAMES = FPS * DURATION

# Ball setup
ball_radius = 4
ball_pos = np.array([WIDTH // 2, HEIGHT // 2] , dtype ='float32')
ball_velocity = np.array([4, 0.0])
gravity = np.array([0, 2])
ball_color = (255, 60, 60)
test_color = (0, 0, 255)

# Ring config
num_rings = 1
ring_spacing = 10
ring_thickness = 3
gap_angle = math.radians(40)

# Output
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_dir = f"escape_game_{timestamp}"
frame_dir = os.path.join(output_dir, "frames")
#os.makedirs(frame_dir, exist_ok=True)

BLACK = (10, 10, 10)
WHITE = (240, 240, 240)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Ring states
ring_angles = math.pi/6#[random.uniform(0,math.pi/6) for _ in range(num_rings)]
ring_rot_speeds = 0.05#[random.uniform(0.005, 0.02) for _ in range(num_rings)]

escaped = False

def is_angle_in_gap(angle, gap_start, gap_size):
    gap_end = (gap_start + gap_size) % (2 * math.pi)
    if gap_start < gap_end:
        return gap_start <= angle <= gap_end
    else:
        return angle >= gap_start or angle <= gap_end


for frame in range(FRAMES):
    screen.fill(BLACK)
    center = np.array([WIDTH // 2, HEIGHT // 2])

    # Draw rotating rings
    # for i in range(num_rings):
    #     radius = 80 + i * ring_spacing
    #     rect = pygame.Rect(center[0] - radius, center[1] - radius, radius * 2, radius * 2)
    #     start_angle = ring_angles[i]
    #     end_angle = start_angle + (2 * math.pi - gap_angle)
    #     pygame.draw.arc(screen, WHITE, rect, start_angle, end_angle, ring_thickness)
    #     ring_angles[i] += ring_rot_speeds[i]

    radius = 100
    rect = pygame.Rect(center[0] - radius, center[1] - radius, radius * 2, radius * 2)
    pygame.draw.arc(screen, WHITE, rect, ring_angles, ring_angles + (2 * math.pi - gap_angle), ring_thickness)
    ring_angles += ring_rot_speeds

    start = np.array([math.cos(ring_angles) * radius, -math.sin(ring_angles) * radius]) + center
    end = np.array([math.cos(ring_angles + (2 * math.pi - gap_angle)) * radius,
                    -math.sin(ring_angles + (2 * math.pi - gap_angle)) * radius]) + center


    a = (end[1] - start[1]) / (end[0] - start[0])
    b = start[1] - a * start[0]


    start /= np.linalg.norm(start)
    end /= np.linalg.norm(end)

    angle = np.arccos(start.dot(end))
    #print(f"{abs(a * ball_pos[0] + b ) - abs(ball_pos[1]) } == {0}")
    if( -0.5 < abs(a * ball_pos[0] + b ) - abs(ball_pos[1]) < 0.5 ):
        print("nop")
    if angle <= 5e-05:
        print("nop: " + str(angle))
        # destroy ring N
    else:
        dir = ball_pos - center
        dist = np.linalg.norm(dir)
        if dist + ball_radius + ring_thickness >= 100 :
            if dist != 0:
                normal = dir / dist
                ball_velocity -= 2 * np.dot(ball_velocity, normal) * normal

    ball_pos += ball_velocity + gravity

    pygame.draw.circle(screen, ball_color, ball_pos.astype(int), ball_radius)

    pygame.display.flip()
    #pygame.image.save(screen, os.path.join(frame_dir, f"frame_{frame:04d}.png"))
    clock.tick(FPS)

pygame.quit()

# Compile video
# video_path = os.path.join(output_dir, "escape_ball_game.mp4")
# with imageio.get_writer(video_path, fps=FPS) as writer:
#     for i in range(FRAMES):
#         img = imageio.imread(os.path.join(frame_dir, f"frame_{i:04d}.png"))
#         writer.append_data(img)

#print("✅ Video saved to:", video_path)

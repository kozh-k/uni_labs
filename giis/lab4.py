import pygame
import numpy as np
import math

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)
LINE_COLOR = (255, 255, 255)
FOCAL_LENGTH = 300
OBJECT_FILE = 'object.txt'

TRANSLATION_STEP = 0.1
ROTATION_STEP = math.radians(2)
SCALE_STEP = 1.05

def translation_matrix(tx, ty, tz):
    return np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ], dtype=float)

def rotation_matrix_x(angle):
    c = math.cos(angle)
    s = math.sin(angle)
    return np.array([
        [1, 0, 0, 0],
        [0, c, -s, 0],
        [0, s, c, 0],
        [0, 0, 0, 1]
    ], dtype=float)

def rotation_matrix_y(angle):
    c = math.cos(angle)
    s = math.sin(angle)
    return np.array([
        [c, 0, s, 0],
        [0, 1, 0, 0],
        [-s, 0, c, 0],
        [0, 0, 0, 1]
    ], dtype=float)

def rotation_matrix_z(angle):
    c = math.cos(angle)
    s = math.sin(angle)
    return np.array([
        [c, -s, 0, 0],
        [s, c, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ], dtype=float)

def scale_matrix(sx, sy, sz):
    return np.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ], dtype=float)

def reflection_matrix_xy():
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, -1, 0],
        [0, 0, 0, 1]
    ], dtype=float)

def reflection_matrix_yz():
    return np.array([
        [-1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ], dtype=float)

def reflection_matrix_xz():
    return np.array([
        [1, 0, 0, 0],
        [0, -1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ], dtype=float)

def load_object_from_file(filename):
    vertices = []
    edges = []
    reading_vertices = True
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if line.lower() == 'edges':
                    reading_vertices = False
                    continue

                parts = line.split()
                if reading_vertices:
                    if len(parts) == 3:
                        vertices.append([float(parts[0]), float(parts[1]), float(parts[2]), 1.0])
                else:
                    if len(parts) == 2:
                        edges.append((int(parts[0]), int(parts[1])))

        return np.array(vertices, dtype=float), edges
    except Exception as e:
        print(f"Error: {e}")
        return None, None

def project(vertices, screen_width, screen_height, focal_length):
    projected_points = []
    center_x = screen_width / 2
    center_y = screen_height / 2

    for vertex in vertices:
        x, y, z, w = vertex
        z_proj = z + focal_length
        if abs(z_proj) < 1e-6:
            z_proj = 1e-6 if z_proj >= 0 else -1e-6

        scale_factor = focal_length / z_proj
        screen_x = int(x * scale_factor + center_x)
        screen_y = int(y * scale_factor + center_y)
        projected_points.append((screen_x, screen_y))

    return projected_points

def draw_object(screen, projected_vertices, edges, color):
    if not edges:
        for point in projected_vertices:
            pygame.draw.circle(screen, color, point, 2)
        return

    for edge in edges:
        v1_idx, v2_idx = edge
        if 0 <= v1_idx < len(projected_vertices) and 0 <= v2_idx < len(projected_vertices):
            pygame.draw.line(screen, color, projected_vertices[v1_idx], projected_vertices[v2_idx], 1)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("3D Transformations")
    clock = pygame.time.Clock()

    vertices, edges = load_object_from_file(OBJECT_FILE)
    if vertices is None:
        pygame.quit()
        return

    initial_translation = translation_matrix(0, 0, 2.5)
    current_vertices = vertices @ initial_translation.T

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                transform_matrix = np.identity(4)
                needs_transform = True

                if event.key == pygame.K_LEFT:
                    transform_matrix = translation_matrix(-TRANSLATION_STEP, 0, 0)
                elif event.key == pygame.K_RIGHT:
                    transform_matrix = translation_matrix(TRANSLATION_STEP, 0, 0)
                elif event.key == pygame.K_UP:
                    transform_matrix = translation_matrix(0, -TRANSLATION_STEP, 0)
                elif event.key == pygame.K_DOWN:
                    transform_matrix = translation_matrix(0, TRANSLATION_STEP, 0)
                elif event.key == pygame.K_PAGEUP:
                    transform_matrix = translation_matrix(0, 0, -TRANSLATION_STEP)
                elif event.key == pygame.K_PAGEDOWN:
                    transform_matrix = translation_matrix(0, 0, TRANSLATION_STEP)
                elif event.key == pygame.K_a:
                    transform_matrix = rotation_matrix_y(ROTATION_STEP)
                elif event.key == pygame.K_d:
                    transform_matrix = rotation_matrix_y(-ROTATION_STEP)
                elif event.key == pygame.K_w:
                    transform_matrix = rotation_matrix_x(ROTATION_STEP)
                elif event.key == pygame.K_s:
                    transform_matrix = rotation_matrix_x(-ROTATION_STEP)
                elif event.key == pygame.K_q:
                    transform_matrix = rotation_matrix_z(ROTATION_STEP)
                elif event.key == pygame.K_e:
                    transform_matrix = rotation_matrix_z(-ROTATION_STEP)
                elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                    transform_matrix = scale_matrix(SCALE_STEP, SCALE_STEP, SCALE_STEP)
                elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    transform_matrix = scale_matrix(1.0/SCALE_STEP, 1.0/SCALE_STEP, 1.0/SCALE_STEP)
                elif event.key == pygame.K_x:
                    transform_matrix = reflection_matrix_xy()
                elif event.key == pygame.K_y:
                    transform_matrix = reflection_matrix_yz()
                elif event.key == pygame.K_z:
                    transform_matrix = reflection_matrix_xz()
                else:
                    needs_transform = False

                if needs_transform:
                    current_vertices = current_vertices @ transform_matrix

        screen.fill(BACKGROUND_COLOR)
        projected_points = project(current_vertices, SCREEN_WIDTH, SCREEN_HEIGHT, FOCAL_LENGTH)
        draw_object(screen, projected_points, edges, LINE_COLOR)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
import pygame
import math
import sys

# Initialize Pygame
pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Spinning Octagon with Bouncing Ball")
clock = pygame.time.Clock()

# Simulation parameters
gravity = 0.5  # downward acceleration
restitution = 0.9  # bounciness on collision (energy retention)
damping = 0.995  # air friction/damping per frame
angular_velocity = 0.01  # radians per frame (for the octagon)

# Octagon parameters
octagon_radius = 250
octagon_center = (screen_width // 2, screen_height // 2)
rotation_angle = 0

# Ball parameters
ball_radius = 15
ball_pos = [octagon_center[0], octagon_center[1]]
ball_vel = [5, -5]  # initial velocity


def get_octagon_vertices(center, radius, angle_offset):
    """Return the list of 8 vertices for an octagon rotated by angle_offset."""
    vertices = []
    for i in range(8):
        angle = angle_offset + i * (2 * math.pi / 8)
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        vertices.append((x, y))
    return vertices


def reflect_velocity(vel, normal, restitution):
    """
    Reflect a 2D velocity vector 'vel' across a surface with given 'normal'.
    The factor (1+restitution) controls energy retention.
    """
    dot = vel[0] * normal[0] + vel[1] * normal[1]
    return [
        vel[0] - (1 + restitution) * dot * normal[0],
        vel[1] - (1 + restitution) * dot * normal[1],
    ]


def process_collision(ball_pos, ball_vel, vertex1, vertex2):
    """
    Check and resolve collision between the ball and a line segment (edge of the octagon).
    Uses the projection of the ball center onto the edge and, if the ball is penetrating,
    reflects its relative velocity (taking into account the moving wall).
    """
    ax, ay = vertex1
    bx, by = vertex2
    # Vector along the edge
    edge_vec = (bx - ax, by - ay)
    # Vector from vertex1 to ball center
    ball_vec = (ball_pos[0] - ax, ball_pos[1] - ay)
    seg_length_sq = edge_vec[0] ** 2 + edge_vec[1] ** 2
    # Projection parameter t (clamped between 0 and 1)
    t = (
        (ball_vec[0] * edge_vec[0] + ball_vec[1] * edge_vec[1]) / seg_length_sq
        if seg_length_sq != 0
        else 0
    )
    t = max(0, min(1, t))
    # Closest point on the edge
    closest_x = ax + t * edge_vec[0]
    closest_y = ay + t * edge_vec[1]
    # Vector from closest point to ball center
    dx = ball_pos[0] - closest_x
    dy = ball_pos[1] - closest_y
    dist = math.hypot(dx, dy)

    if dist < ball_radius:
        # Compute the normal (avoid division by zero)
        if dist == 0:
            # Use an arbitrary perpendicular vector if the ball is exactly on the edge.
            n = (-edge_vec[1], edge_vec[0])
            n_len = math.hypot(n[0], n[1])
            n = (n[0] / n_len, n[1] / n_len)
        else:
            n = (dx / dist, dy / dist)

        # Compute the edge velocity at the collision point.
        # For a rotating octagon, the velocity at a point is given by
        # v_edge = angular_velocity * (perpendicular to r), where r = collision point - octagon_center.
        rx = closest_x - octagon_center[0]
        ry = closest_y - octagon_center[1]
        # The perpendicular (for a counterclockwise rotation) is (-ry, rx)
        edge_vel = [angular_velocity * (-ry), angular_velocity * (rx)]

        # Compute the ball's velocity relative to the moving wall.
        rel_vel = [ball_vel[0] - edge_vel[0], ball_vel[1] - edge_vel[1]]
        # Only reflect if the ball is moving toward the wall.
        if (rel_vel[0] * n[0] + rel_vel[1] * n[1]) < 0:
            # Reflect the relative velocity.
            reflected = reflect_velocity(rel_vel, n, restitution)
            # New ball velocity is the reflected relative velocity plus the wall's velocity.
            ball_vel[0] = reflected[0] + edge_vel[0]
            ball_vel[1] = reflected[1] + edge_vel[1]

            # Correct the ball position to prevent sinking into the wall.
            penetration = ball_radius - dist
            ball_pos[0] += n[0] * penetration
            ball_pos[1] += n[1] * penetration


# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update the octagon's rotation angle.
    rotation_angle += angular_velocity
    octagon_vertices = get_octagon_vertices(
        octagon_center, octagon_radius, rotation_angle
    )

    # Update ball physics.
    ball_vel[1] += gravity  # apply gravity
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # Check for collisions against each edge of the octagon.
    for i in range(len(octagon_vertices)):
        vertex1 = octagon_vertices[i]
        vertex2 = octagon_vertices[(i + 1) % len(octagon_vertices)]
        process_collision(ball_pos, ball_vel, vertex1, vertex2)

    # Apply damping to simulate air friction.
    ball_vel[0] *= damping
    ball_vel[1] *= damping

    # Draw background, octagon, and ball.
    screen.fill((30, 30, 30))
    pygame.draw.polygon(screen, (200, 200, 200), octagon_vertices, 3)
    pygame.draw.circle(
        screen, (255, 100, 100), (int(ball_pos[0]), int(ball_pos[1])), ball_radius
    )

    pygame.display.flip()
    clock.tick(60)

        for i in range(len(enemie)):
            ex, ey, ez = enemie[i]

            # Direction vector towards player
            dx = player_x - ex
            dy = player_y - ey

            # Distance to normalize
            dist = math.sqrt(dx*dx + dy*dy)

            if dist > 0:  # prevent divide by zero
                dx /= dist
                dy /= dist

            # Move enemy a little step toward player
            ex += (dx * enemie_moving_unit) * 0.1
            ey += (dy * enemie_moving_unit) * 0.1

            # Save new position
            enemie[i] = [ex, ey, ez]
    def is_hit_by(self, bullet):
        if not self.active or not bullet.active or self.hit:
            return False

        # Check if bullet crosses the target's z-plane between frames
        prev_z = bullet.z - bullet.dz
        # If bullet moved past the target's z position this frame
        if (prev_z > self.z and bullet.z <= self.z) or abs(bullet.z - self.z) < bullet.dz:
            # Check (x, y) distance at the z-plane of the target
            # Interpolate bullet position at target z
            t = (self.z - prev_z) / (bullet.z - prev_z) if bullet.z != prev_z else 0
            bx = bullet.x - bullet.dx + bullet.dx * t
            by = bullet.y - bullet.dy + bullet.dy * t
            dx = self.x - bx
            dy = self.y - by
            distance = math.sqrt(dx*dx + dy*dy)
            return distance <= self.size
        return False
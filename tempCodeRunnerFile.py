    def check_collision(self, bullet):
        if not self.active or not bullet.active or self.hit:
            return 0

        # 3D distance between bullet and target center
        distance = math.sqrt(
            (self.x - bullet.x)**2 +
            (self.y - bullet.y)**2 +
            (self.z - bullet.z)**2
        )

        # Target hit if within target size
        if distance <= self.size * 0.3:  # Bullseye
            self.hit = True
            bullet.active = False
            return 10
        elif distance <= self.size * 0.5:
            self.hit = True
            bullet.active = False
            return 9
        elif distance <= self.size * 0.7:
            self.hit = True
            bullet.active = False
            return 7
        elif distance <= self.size * 0.9:
            self.hit = True
            bullet.active = False
            return 5
        elif distance <= self.size:
            self.hit = True
            bullet.active = False
            return 1

        return 0
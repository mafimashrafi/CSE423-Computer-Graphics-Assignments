        rain_x = random.randint(0, window_width)
        rain_y = random.randint(0, window_height)
        rain = Rain(rain_x, rain_y)

        rain_R = random.random()
        rain_G = random.random()
        rain_B = random.random()
        rain.draw_raindrop(rain_R, rain_G, rain_B)
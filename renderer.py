from time import sleep
from opc import Client
from threading import Thread
import settings


class Renderer(object):
    def __init__(self):
        self.client = Client(settings.FC_SERVER + ':' + str(settings.FC_PORT))
        self.brightness = 0.5
        self.pixels = [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1]
        ]
        self.render_pixels = self.calculate_pixels()
        self.render_thread = Thread(target=self.render)
        self.render_thread.daemon = True
        self.render_thread.start()

    def calculate_pixels(self):
        ret_val = []
        for pixel in self.pixels:
            px = [(
                int(pixel[0] * self.brightness * settings.RGB_MAX),
                int(pixel[1] * self.brightness * settings.RGB_MAX),
                int(pixel[2] * self.brightness * settings.RGB_MAX)
             )] * settings.PIXEL_COUNT

            ret_val.extend(px)
        return ret_val

    def update(self):
        self.render_pixels = self.calculate_pixels()

    def render(self):
        while True:
            self.client.put_pixels(self.render_pixels)
            sleep(1.0 / settings.FRAMES)

from opc import Client
from flask import Flask, request

BOX_COUNT = 4
RGB_COUNT = 3
PIXEL_COUNT = 15
RGB_MAX = 255
DEBUG = False

app = Flask(__name__)
app.debug = DEBUG

client = Client('localhost:7890')

brightness = 0.5
pixels = [
    [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]
]


@app.route("/brightness", methods=['GET'])
def route_brightness():
    global brightness
    try:
        brightness = float(request.args.get('value'))
        render()
        return '', 201
    except ValueError:
        return 'Invalid brightness', 400


@app.route("/pixels", methods=['POST'])
def route_pixels():
    global pixels

    json_pixels = request.get_json(silent=True)

    if not json_pixels:
        return 'Invalid pixels', 400

    if len(json_pixels) != BOX_COUNT:
        return 'Invalid pixel count (%i expected %i)' % (len(json_pixels), BOX_COUNT), 400

    for json_pixel in json_pixels:
        if len(json_pixel) != RGB_COUNT:
            return 'Invalid rgb count (%i expected %i)' % (len(json_pixel), RGB_COUNT), 400

        for color in json_pixel:
            if color < 0 or color > 1:
                return 'Invalid rgb value %s' % (color,), 400

    pixels = json_pixels

    render()

    return '', 201


def render():
    render_pixels = []
    for pixel in pixels:
        px = [(
            int(pixel[0] * brightness * RGB_MAX),
            int(pixel[1] * brightness * RGB_MAX),
            int(pixel[2] * brightness * RGB_MAX)
         )] * PIXEL_COUNT

        render_pixels.extend(px)
    client.put_pixels(render_pixels)

render()

if __name__ == "__main__":
    app.run()

from json import dumps
from renderer import Renderer
from flask import Flask, request
import settings


app = Flask(import_name=__name__,
            static_folder=settings.STATIC_FOLDER,
            static_url_path=settings.STATIC_URL)

app.debug = settings.DEBUG
app.renderer = Renderer()


@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('index.html')


@app.route('/values', methods=['GET'])
def route_values():
    res = {
        'brightness': app.renderer.brightness,
        'pixels': app.renderer.pixels
    }

    return dumps(res), 200


@app.route("/brightness", methods=['GET'])
def route_brightness():
    try:
        app.renderer.brightness = float(request.args.get('value'))
        app.renderer.update()
        return '', 201
    except ValueError:
        return 'Invalid brightness', 400


@app.route("/pixels", methods=['POST'])
def route_pixels():
    json_pixels = request.get_json(silent=True)

    if not json_pixels:
        return 'Invalid pixels', 400

    if len(json_pixels) != settings.BOX_COUNT:
        return 'Invalid pixel count (%i expected %i)' % (len(json_pixels), settings.BOX_COUNT), 400

    for json_pixel in json_pixels:
        if len(json_pixel) != settings.RGB_COUNT:
            return 'Invalid rgb count (%i expected %i)' % (len(json_pixel), settings.RGB_COUNT), 400

        for color in json_pixel:
            if color < 0 or color > 1:
                return 'Invalid rgb value %s' % (color,), 400

    app.renderer.pixels = json_pixels
    app.renderer.update()

    return '', 201

if __name__ == "__main__":
    app.run()

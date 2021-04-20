from Class.Application import Application as app
from Models.Sound import Sound
from flask import jsonify, make_response
from Class.Interfase.IController import IController
from Class.MakeResponse import MakeResponse


class LoadMusicController(IController):
    def __call__(self, massed, *args, **kwargs):
        req = massed.get_json()
        sounds = app().context.query(Sound).all()[req["start"]:req["end"]]
        sounds = list(map(lambda x: MakeResponse.make_response_sound(x.__dict__), sounds))
        res = make_response(jsonify({"data": sounds}), 200)
        return res



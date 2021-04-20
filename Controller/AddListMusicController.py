from Class.Application import Application as app
from Models.ListSound import ListSound
from flask import jsonify, make_response, url_for
from Class.Interfase.IController import IController
from flask_login import current_user
from Class.MakeResponse import MakeResponse
import pickle


class AddListMusicController(IController):
    def __call__(self, massed, *args, **kwargs):
        req = massed.get_json()
        user = app().context.query(ListSound).filter(ListSound.id_user == current_user.id).first()
        if user is None:
            list_sound = ListSound(id_user=current_user.id,
                                   name="Мой плейлист")
            app().context.add(list_sound)
            app().context.commit()
        list_sound = app().context.query(ListSound).filter(ListSound.id_user == current_user.id).first()

        list_sound_dump = pickle.loads(list_sound.sounds)
        list_sound_dump.append(req["id"])
        list_sound.sounds = pickle.dumps(list_sound_dump)

        app().context.commit()
        res = make_response(jsonify({"data": "succesfull"}), 200)
        return res

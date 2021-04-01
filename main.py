from Class.Application import Application

from Controller.LoginController import LoginController
from Controller.ReqistrationController import ReqistrationController
from Controller.UploadMusicController import UploadMusicController
from Controller.ProfileController import MyProfileController

from forms.LoginForm import LoginForm
from forms.ReqistrationForm import RegisterForm
from forms.UploadMusicForm import UploadMusicForm
from forms.ProfileForm import ProfileForm

from Models.User import User

import os

from flask import Flask, render_template, redirect, request, abort, session
from flask_login import login_user, logout_user, login_required
from sqlalchemy import desc
from forms.comment import Comment
from forms.fake_quest import Fake_Quest
import datetime

Application().app = Flask(__name__)
app = Application().app

app.config["FILE_DIR"] = os.path.dirname(os.path.abspath(__file__))

login_manager = Application().login_manager


@login_manager.user_loader
def load_user(user_id):
    db_sess = Application().context
    return db_sess.query(User).get(user_id)


@app.route("/", methods=['GET', 'POST'])
def index():
    db_sess = Application().context
    #quest_list = db_sess.query(Quest).order_by(desc(Quest.created_date))
    state = 'Новые квесты'
    if request.method == 'POST':
        if "new" in request.form:
            state = 'Новые квесты'
            #quest_list = db_sess.query(Quest).order_by(desc(Quest.created_date))
        elif 'views' in request.form:
            state = 'По просмотрам'
            #quest_list = db_sess.query(Quest).order_by(desc(Quest.views))
        elif 'likes' in request.form:
            state = 'По лайкам/дизлайкам'
            #quest_list = db_sess.query(Quest).order_by(desc(Quest.likes - Quest.dislikes))
        elif 'my' in request.form:
            state = 'Мои квесты'
            #quest_list = db_sess.query(Quest).filter(Quest.user_id == current_user.id).order_by(desc(Quest.created_date))
        elif 'search' in request.form:
            state = 'Найденные по запросу квесты'
            #quest_list = db_sess.query(Quest).filter(Quest.title.like(f'%{request.form.get("text")}%')).order_by(desc(Quest.created_date))
    return render_template("index.html", title='Fairy Tale', quest_list=[], state=state)


@app.route("/upload_music",  methods=['GET', 'POST'])
@login_required
def upload_music():
    controller = UploadMusicController(model=UploadMusicForm())
    return controller()


@app.route("/my_profile",  methods=['GET', 'POST'])
@login_required
def my_profile():
    controller = MyProfileController(model=ProfileForm())
    return controller()


@app.route('/login', methods=['GET', 'POST'])
def login():
    controller = LoginController(model=LoginForm(), login_user=login_user)
    return controller()


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    controller = ReqistrationController(model=RegisterForm(), login_user=login_user)
    return controller()


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


'''@app.route('/quest/<int:quest_id>', methods=['GET', 'POST'])
def quest_main_page(quest_id):
    db_sess = Application().context
    quest = db_sess.query(Quest).filter(Quest.id == quest_id).first()
    if not quest:
        abort(404)

    comments = db_sess.query(Commentary).filter(Commentary.quest_id == quest_id).order_by(desc(Commentary.created_date))
    
    if f'{quest_id}viewed' not in session:
        quest.views += 1
        session[f'{quest_id}viewed'] = 1            
        db_sess.commit()
        
    state = 'none'
    if current_user.is_authenticated:
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        if str(quest_id) in user.like.split():
            state = 'liked'
        elif str(quest_id) in user.dislike.split():
            state = 'disliked'
        else:
            state = 'none'
        
    if request.method == 'POST':
        if "like" in request.form:
            if state == 'liked':
                t = user.like.split()
                t.remove(str(quest_id))
                user.like = ' '.join(t)
                quest.likes -= 1
            else:
                user.like += ' ' + str(quest_id)
                quest.likes += 1
                if state == 'disliked':
                    t = user.dislike.split()
                    t.remove(str(quest_id))
                    user.dislike = ' '.join(t)
                    quest.dislikes -= 1
        elif "dislike" in request.form:
            if state == 'disliked':
                t = user.dislike.split()
                t.remove(str(quest_id))
                user.dislike = ' '.join(t)
                quest.dislikes -= 1
            else:
                user.dislike += ' ' + str(quest_id)
                quest.dislikes += 1
                if state == 'liked':
                    t = user.like.split()
                    t.remove(str(quest_id))
                    user.like = ' '.join(t)
                    quest.likes -= 1
        db_sess.commit()
        return redirect(f'/quest/{quest_id}')
        
    return render_template("quest_main_page.html", title=quest.title, quest=quest, comments=comments, state=state)


@app.route('/quest/<int:quest_id>/commenting', methods=['GET', 'POST'])
@login_required
def add_commentary(quest_id):
    form = Comment()
    if form.validate_on_submit():
        db_sess = Application().context
        commentary = Commentary()
        commentary.content = form.content.data
        commentary.quest_id = quest_id
        current_user.commentary.append(commentary)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect(f'/quest/{quest_id}')
    return render_template('commenting.html', title='Добавление комментария', 
                           form=form)


@app.route('/quest/<int:quest_id>/commenting/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_comment(quest_id, id):
    form = Comment()
    if request.method == "GET":
        db_sess = Application().context
        commentary = db_sess.query(Commentary).filter(Commentary.id == id,
                                          Commentary.user == current_user
                                          ).first()
        if current_user.moderation:
            commentary = db_sess.query(Commentary).filter(Commentary.id == id).first()            
        if commentary:
            form.content.data = commentary.content
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        commentary = db_sess.query(Commentary).filter(Commentary.id == id,
                                          Commentary.user == current_user
                                          ).first()
        if current_user.moderation:
            commentary = db_sess.query(Commentary).filter(Commentary.id == id).first()        
        if commentary:
            commentary.content = form.content.data
            commentary.edited = True
            db_sess.commit()
            return redirect(f'/quest/{quest_id}')
        else:
            abort(404)
    return render_template('commenting.html',
                           title='Редактирование комментария',
                           form=form
                           )


@app.route('/quest/<int:quest_id>/delete_commentary/<int:id>', methods=['GET', 'POST'])
@login_required
def comment_delete(quest_id, id):
    db_sess = Application().context
    commentary = db_sess.query(Commentary).filter(Commentary.id == id,
                                      Commentary.user == current_user
                                      ).first()
    if current_user.moderation:
        commentary = db_sess.query(Commentary).filter(Commentary.id == id).first()    
    if commentary:
        db_sess.delete(commentary)
        db_sess.commit()
    else:
        abort(404)
    return redirect(f'/quest/{quest_id}')


@app.route('/quest_constructor', methods=['GET', 'POST'])
@login_required
def add_quest():
    form = Fake_Quest()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        quest = Quest()
        quest.title = form.title.data
        quest.description = form.description.data
        current_user.quests.append(quest)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('fake_quest_constructor.html', title='Создание квеста', 
                           form=form)


@app.route('/quest_constructor/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_quest(id):
    form = Fake_Quest()
    if request.method == "GET":
        db_sess = Application().context
        quest = db_sess.query(Quest).filter(Quest.id == id,
                                          Quest.user == current_user
                                          ).first()
        if current_user.moderation:
            quest = db_sess.query(Quest).filter(Quest.id == id).first()            
        if quest:
            form.title.data = quest.title
            form.description.data = quest.description
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        quest = db_sess.query(Quest).filter(Quest.id == id,
                                          Quest.user == current_user
                                          ).first()
        if current_user.moderation:
            quest = db_sess.query(Quest).filter(Quest.id == id).first()       
        if quest:
            quest.title = form.title.data
            quest.description = form.description.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('fake_quest_constructor.html',
                           title='Редактирование квеста',
                           form=form
                           )


@app.route('/quest_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def quest_delete(id):
    db_sess = Application().context
    quest = db_sess.query(Quest).filter(Quest.id == id,
                                          Quest.user == current_user
                                          ).first()
    if current_user.moderation:
        quest = db_sess.query(Quest).filter(Quest.id == id).first()     
    if quest:
        db_sess.delete(quest)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')

'''


def main():
    Application().create_context("db/sound.db")
    app.run(debug=True)


if __name__ == '__main__':
    main()

from Class.Application import Application
from Controller.LoginController import LoginController

from flask import Flask, render_template, redirect, request, abort, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy import desc
from data import db_session
from data.users import User
from Models.User import User
from data.quests import Quest
from data.commentary import Commentary
from forms.user import RegisterForm
from forms.LoginForm import LoginForm
from forms.comment import Comment
from forms.fake_quest import Fake_Quest
import datetime

Application().app = Flask(__name__)
app = Application().app

login_manager = Application().login_manager


@login_manager.user_loader
def load_user(user_id):
    db_sess = Application().context
    return db_sess.query(User).get(user_id)


@app.route("/", methods=['GET', 'POST'])
def index():
    db_sess = Application().context
    quest_list = db_sess.query(Quest).order_by(desc(Quest.created_date))
    state = 'Новые квесты'
    if request.method == 'POST':
        if "new" in request.form:
            state = 'Новые квесты'
            quest_list = db_sess.query(Quest).order_by(desc(Quest.created_date))
        elif 'views' in request.form:
            state = 'По просмотрам'
            quest_list = db_sess.query(Quest).order_by(desc(Quest.views))
        elif 'likes' in request.form:
            state = 'По лайкам/дизлайкам'
            quest_list = db_sess.query(Quest).order_by(desc(Quest.likes - Quest.dislikes))
        elif 'my' in request.form:
            state = 'Мои квесты'
            quest_list = db_sess.query(Quest).filter(Quest.user_id == current_user.id).order_by(desc(Quest.created_date))
        elif 'search' in request.form:
            state = 'Найденные по запросу квесты'
            quest_list = db_sess.query(Quest).filter(Quest.title.like(f'%{request.form.get("text")}%')).order_by(desc(Quest.created_date))
    return render_template("index.html", title='Fairy Tale', quest_list=quest_list, state=state)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = Application().context
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user, remember=True)
        return redirect("/")
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = Application().context
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/test/login', methods=['GET', 'POST'])
def test_login():
    controller = LoginController(None, None, login_user)
    return controller()


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/quest/<int:quest_id>', methods=['GET', 'POST'])
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


def main():
    Application().create_context("db/sound.db")
    #db_session.global_init("db/quests_db.db")
    app.run(debug=True)


if __name__ == '__main__':
    main()

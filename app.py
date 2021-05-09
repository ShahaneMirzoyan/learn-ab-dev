from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import traceback
from config import Configuration
# from flask_wtf.csrf import CsrfProtect
# csrf = CsrfProtect()

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from forms import QuestionForm
from functions import _set_is_final, _set_qid_and_current_question

#from datetime import datetime

app = Flask(__name__)
app.config.from_object(Configuration)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

from models import *

@app.route('/')
def index():
    posts = Post.query.order_by(Post.is_practice.asc()).all()
    return render_template("index.html", posts = posts[:])


@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/test')
def test():
    return render_template("test.html")

@app.route('/submit-results', methods = ['POST', 'GET'])
def submit_results():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        is_practice = False
        article = Post(title = title, text = text, is_practice= is_practice)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect(url_for('index'))
        except:
            traceback.print_exc()
            return 'foo'

    return render_template("submit-results.html")



@app.route('/posts/<int:id>', methods = ['POST', 'GET'])
def post_detail(id):
    post = Post.query.get(id)
    if post.is_practice:
        questions = post.questions
        qid, current_question = _set_qid_and_current_question(request.args.get('qid'), questions)
        form = QuestionForm(current_question)

        if request.method == 'POST':
            if form.validate_on_submit():
                user_answer = request.form['user_answer']
                if user_answer == current_question.answer:
                    is_final = qid == len(questions)
                    if is_final:
                        flash('Вы ответили на последний вопрос блока, congrats!')
                        return redirect(url_for('index'))


                    return redirect(url_for('post_detail', qid = qid+1, id = id))
    else:
        form, qid = None, None
    return render_template("post_detail.html", post = post,
                            form = form, qid = qid)

# if __name__ == "__main__":
#     app.run(debug=True)




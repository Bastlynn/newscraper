from flask import Flask, render_template, flash, request, redirect, url_for
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

import subprocess
# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
import shlex


class ReusableForm(Form):
    name = TextField('https://www.', validators=[validators.required()])


from time import sleep


@app.route("/results", methods=['GET', 'POST'])
def view_results():
    pass


@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)

    print(form.errors)
    if request.method == 'POST':
        name = request.form['name']
        print(name)

        if form.validate():

            def run_command(name):

                process = subprocess.Popen(
                    shlex.split('python3 cosine_finder.py https://www.{}'.format(name)),
                    stdout=subprocess.PIPE)
                lines = ''
                for line in iter(process.stdout.readline, ''):
                    ln = line.decode('utf-8')
                    lines += '\n' + ln
                    if ln == '':
                        if process.poll() is not None:
                            break
                    else:
                        print(ln)
                        flash(ln)

            run_command(name)

            return render_template('index.html', form=form)
            # Save the comment here.

        else:
            flash('All the form fields are required. ')

    return render_template('submit.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)

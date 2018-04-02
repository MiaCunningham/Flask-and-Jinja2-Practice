from flask import Flask, request, redirect, render_template
import os
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route("/validate-time")
def display_time_form():
    return render_template('time_form.html')


def is_integer(num):
    try:
        int(num)
        return True
    except ValueError:
        return False

@app.route('/validate-time', methods=['POST'])
def validate_time():
    hours = request.form['hours']
    minutes = request.form['minutes']

    hours_error = ''
    minutes_error = ''

    if not is_integer(hours):
        hours_error = 'Not a valid integer'
        hours = ''
    else:
        hours = int(hours)
        if hours>23 or hours < 0:
            hours_error = 'Hours value out of range'

    if not is_integer(minutes):
        minutes_error = 'Not a valid integer'
        minutes = ''
    else:
        minutes = int(minutes)
        if minutes > 59 or minutes < 0:
            minutes_error = 'miutes out of range'


    if not minutes_error and not hours_error:
        time = str(hours) + ' : ' + str(minutes)

        return redirect("/valid-time?time={0}".format(time))
    else:
        return render_template('time_form.html',
            hours_error = hours_error,
            minutes_error = minutes_error,
            hours = hours,
            minutes = minutes)



@app.route('/valid-time')
def valid_time():
    time = request.args.get('time')
    return render_template('valid_time.html', time = time)


@app.route("/")
def  index():
    return render_template('hello_form.html')


@app.route('/hello', methods= ['POST'])
def  hello():
    first_name = request.form['first_name']
    return render_template('greeting_form.html', name = first_name)

tasks = []

@app.route('/todos', methods= ['POST', 'GET'])
def todo():
    if request.method == 'POST':
        task = request.form['task']
        tasks.append(task)

    return render_template('todos.html', tasks = tasks, title="TO DOs")

app.run()
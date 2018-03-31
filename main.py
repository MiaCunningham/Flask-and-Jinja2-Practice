from flask import Flask, request, redirect
import os
import jinja2
import cgi

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route("/validate-time")
def display_time_form():
    template = jinja_env.get_template('time_form.html')
    return template.render()


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
        template = jinja_env.get_template('time_form.html')
        return template.render(hours_error = hours_error,
            minutes_error = minutes_error, 
            hours = hours,
            minutes = minutes)



@app.route('/valid-time')
def valid_time():
    time = request.args.get('time')
    template = jinja_env.get_template('valid_time.html')
    return template.render(time = time)


@app.route("/")
def  index():
    template = jinja_env.get_template('hello_form.html')
    return template.render()

@app.route('/hello', methods= ['POST'])
def  hello():
    first_name = request.form['first_name']
    template = jinja_env.get_template('greeting_form.html')

    return template.render(name = first_name)


app.run()
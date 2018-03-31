from flask import Flask, request, redirect
import cgi
app = Flask(__name__)

app.config['DEBUG'] = True


time_form = """
<style>
    .error {{color: red}}
</style>
<form method="POST">
    <label for="hours">hours
        <input type="text" name="hours" value={hours}>
    </label>
    <p class="error">{hours_error}</p>
    <label for="minutes"> Minutes
        <input type="text" name="minutes" value={minutes}>
    </label>
    <p class="error">{minutes_error}</p>
    <input type="submit" value="validate">
</form>
"""

@app.route('/validate-time')
def display_time_form():
    return time_form.format(hours='', hours_error='', minutes='',minutes_error='')



def is_integer(num):
    try:
        int(num)
        return True
    except ValueError:
        return False
    
@app.route('/validate-time', methods = ['POST', 'GET'])
def validate_time():
    hours = request.form['hours']
    minutes = request.form['minutes']

    hours_error = ''
    minutes_error = ''

    if not is_integer(hours):
        hours_error = 'Not a valid integer'
        hours_error = ''
    else:
        hours = int(hours)
        if hours < 0 or hours > 23:
            hours_error = "Hours out of bound (0-23)"
    if not is_integer(minutes):
        minutes_error = 'Not a valid integer'
    else:
        minutes = int(minutes)
        if minutes > 59 or minutes < 0:
            minutes_error = 'Minutes out of range(0-60)'
    
    if not hours_error and not minutes_error:
        time = str(hours) + " : " + str(minutes)

        return redirect("/valid-time?time={0}".format(time))
    else:
        return time_form.format(hours = hours, hours_error = hours_error,
                minutes = minutes, minutes_error = minutes_error)
    

@app.route('/valid-time')
def valid_time():
    time = request.args.get('time')
    return "<h1>You entered {0}. Thank you!</h1>".format(time)


app.run()
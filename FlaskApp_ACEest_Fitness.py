flask_fitness_app/

 app.py
 templates/
    index.html
   workouts.html
   static/
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Store workouts in memory (for now)
workouts = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_workout():
    workout = request.form['workout']
    duration = request.form['duration']

    if not workout or not duration:
        return "Please enter both workout and duration", 400

    try:
        duration = int(duration)
        workouts.append({"workout": workout, "duration": duration})
    except ValueError:
        return "Duration must be a number", 400

    return redirect(url_for('view_workouts'))

@app.route('/workouts')
def view_workouts():
    return render_template('workouts.html', workouts=workouts)

if __name__ == '__main__':
    app.run(debug=True)
<!DOCTYPE html>
<html>
<head>
    <title>ACEestFitness and Gym</title>
</head>
<body>
    <h1>ACEestFitness and Gym</h1>
    <form method="POST" action="/add">
        <label>Workout:</label>
        <input type="text" name="workout" required><br><br>

        <label>Duration (minutes):</label>
        <input type="number" name="duration" required><br><br>

        <button type="submit">Add Workout</button>
    </form>

    <br>
    <a href="/workouts">View Workouts</a>
</body>
</html>
<!DOCTYPE html>
<html>
<head>
    <title>Logged Workouts</title>
</head>
<body>
    <h1>Logged Workouts</h1>
    {% if workouts %}
        <ul>
        {% for entry in workouts %}
            <li>{{ loop.index }}. {{ entry.workout }} - {{ entry.duration }} minutes</li>
        {% endfor %}
        </ul>
    {% else %}
        <p>No workouts logged yet.</p>
    {% endif %}

    <a href="/">Go Back</a>
</body>
</html>

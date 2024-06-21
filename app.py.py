from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

def calculate_time_at_10_knots(remaining_distance, travel_time_at_12_knots, fullspeed, ecospeed):
    distance_at_12_knots = (fullspeed * travel_time_at_12_knots)
    remaining_distance_at_10_knots = remaining_distance - distance_at_12_knots
    travel_time_at_10_knots = remaining_distance_at_10_knots / ecospeed
    total_time_at_10_knots = travel_time_at_10_knots
    return total_time_at_10_knots

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    remaining_distance = int(request.form['remaining_distance'])
    time1 = datetime.fromisoformat(request.form['time1'])
    time2 = datetime.fromisoformat(request.form['time2'])
    travel_time_at_12_knots = int(request.form['travel_time_at_12_knots'])
    fullspeed = float(request.form['fullspeed'])  # 使用float()来处理包含小数的输入值
    ecospeed = float(request.form['ecospeed'])  # 使用float()来处理包含小数的输入值

    hour_difference = (time2 - time1).total_seconds() / 3600
    hour_difference = round(hour_difference, 1)
    time_at_10_knots = calculate_time_at_10_knots(remaining_distance, travel_time_at_12_knots, fullspeed, ecospeed)
    time_at_10_knots = round(time_at_10_knots, 2)



    new_time = time1 + timedelta(hours=travel_time_at_12_knots) + timedelta(hours=time_at_10_knots)

    result_data = {
        'hour_difference': hour_difference,
        'time_at_10_knots': time_at_10_knots,
        'new_time': new_time.strftime("%Y-%m-%d %H:%M")
    }

    return jsonify(result_data)

if __name__ == '__main__':
    app.run(debug=True)


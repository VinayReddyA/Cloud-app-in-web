from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('display.html')

    if request.method == "POST":
        name = request.form['filename']
        try:
            with open(name, "r") as lines:
                total_time_spend = 0
                for line in lines:
                    if line.find("Time Log:") == 0:
                        continue
                    if 'am' not in line.lower() and 'pm' not in line.lower():
                        continue
                    started_time = datetime.strptime(line.split('-')[0].strip()[-7:].lower().strip(), '%I:%M%p')
                    end_time = datetime.strptime(line.split('-')[1][1:8].lower().strip(), '%I:%M%p')
                    time_spend = end_time - started_time
                    total_time = total_time_spend + (time_spend.seconds / 60)
               
                return render_template('display.html',
                                    file_name = name.split('.')[0],
                                    result='{:02d} hours {:02d} minutes'.format(*divmod(int(total_time), 60)))
        except FileNotFoundError:
            message = "Sorry, Choose   file."
            return render_template('display.html', file_not_found_error = message)

if __name__ == '__main__':
    app.run(debug=True)

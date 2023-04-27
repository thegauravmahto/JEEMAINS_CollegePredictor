from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Read data from the CSV file
data = pd.read_csv("data.csv")

# Define a function to predict college based on rank, caste, state, branch, and gender
def predict_college(rank, caste, state, branch, gender):
    if gender.lower() == 'male':
        filtered_data = data[(data['Max_Rank'] >= rank) & (data['Gender'] == 'Gender-Neutral')]
    elif gender.lower() == 'female':
        filtered_data = data[(data['Max_Rank'] >= rank) & (data['Gender'].isin(['Gender-Neutral', 'Female-only (including Supernumerary)']))]
    else:
        filtered_data = pd.DataFrame()

    if state != "":
        filtered_data = filtered_data[filtered_data['State'] == state]
    
    if branch != "":
        filtered_data = filtered_data[filtered_data['Branch'] == branch]

    if caste != "":
        filtered_data = filtered_data[filtered_data['Caste'] == caste]

    return filtered_data


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    rank = int(request.form['rank'])
    caste = request.form['caste']
    state = request.form['state']
    branch = request.form['branch']
    gender = request.form['gender']

    result = predict_college(rank, caste, state, branch, gender)

    if not result.empty:
        result = result[['College', 'Branch', 'Quota', 'Gender', 'Min_Rank', 'Max_Rank']].to_html(classes='table table-striped', index=False)
        return render_template('result.html', table=result)
    else:
        message = "Sorry, no colleges or programs are available based on your input. Please try again with different inputs."
        return render_template('error.html', message=message)


if __name__ == '__main__':
    app.run(debug=True)

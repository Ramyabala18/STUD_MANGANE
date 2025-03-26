from flask import Flask, render_template_string, request
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

app = Flask(__name__)

# Load the dataset
data = pd.read_csv("Survey_AI.csv")

# Load HTML files from the same directory
def load_html(filename):
    with open(filename, 'r') as file:
        return file.read()

# Route for homepage
@app.route('/')
def home():
    html = load_html('index.html')
    return render_template_string(html)

# Route to display dataset stats
@app.route('/stats')
def stats():
    desc = data.describe(include='all').to_html(classes='table table-striped')
    shape = data.shape
    html = load_html('stats.html')
    return render_template_string(html, shape=shape, desc=desc)

# Route to visualize plots
@app.route('/visuals')
def visuals():
    if not os.path.exists('static'):
        os.makedirs('static')

    # Example 1: Countplot for categorical columns
    categorical_columns = data.select_dtypes(include=['object']).columns
    for col in categorical_columns:
        plt.figure(figsize=(8,5))
        sns.countplot(x=col, data=data)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'static/{col}_countplot.png')
        plt.close()

    # Example 2: Correlation heatmap (if numeric data exists)
    numeric_data = data.select_dtypes(include=['float64', 'int64'])
    if not numeric_data.empty:
        plt.figure(figsize=(10,8))
        sns.heatmap(numeric_data.corr(), annot=True, cmap='coolwarm')
        plt.title('Correlation Heatmap')
        plt.tight_layout()
        plt.savefig('static/corr_heatmap.png')
        plt.close()

    html = load_html('visuals.html')
    return render_template_string(html, categorical_columns=categorical_columns)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

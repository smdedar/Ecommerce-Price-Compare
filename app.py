from flask import Flask, render_template, request
import script

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def index():
    return render_template('search.html')

@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        text = request.form.get('text', '').strip()
        if text:
            processed_text = text.upper()
            script.search(processed_text)
            return render_template('result.html')
        else:
            return render_template('search.html', error="Please enter a search term.")

@app.route('/result')
def result():
    return render_template('result.html')

if __name__ == "__main__":
    app.run(debug=True)
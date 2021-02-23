from flask import Flask, render_template, request
import script
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def index():
    return render_template('search.html')

@app.route('/', methods=['POST'])
def my_form_post():
    if request.method == 'POST':
        text = request.form['text']
        processed_text = text.upper()
        script.search(processed_text)
        return render_template('pickaboo.html')


@app.route('/result')
def result():
    #product = "samsung"
    #script.search(product)
    return render_template('pickaboo.html')
    
        


if __name__ == "__main__":
    app.run(debug=True)


#TO DO:: Import Another Python File in Flask
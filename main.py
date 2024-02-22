from flask import Flask, request, jsonify, render_template
import logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

@app.route('/')
def index():
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
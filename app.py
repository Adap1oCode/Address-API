from flask import Flask, request
from api_integration import get_autocomplete_results

app = Flask(__name__)

@app.route('/print_api_response/<postcode>/<user>')
def print_api_response(postcode,user):
    response = get_autocomplete_results(postcode,user)
    return response

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, render_template
import re

app = Flask(__name__)

def validate_id(id_number):
    if len(id_number) != 10:
        return False

    first_char = id_number[0]
    if not first_char.isalpha():
        return False

    if not id_number[1:].isdigit():
        return False

    # Convert first character to corresponding number
    first_digit = ord(first_char.upper()) - ord('A') + 10

    # Multiply the converted first character by 1 and 9
    sum_product = first_digit * 1 + first_digit * 9

    # Multiply the next 8 digits by 8, 7, 6, 5, 4, 3, 2, 1
    for i in range(1, 9):
        sum_product += int(id_number[i]) * (9 - i)

    # Add the last digit
    sum_product += int(id_number[-1])

    # Check if divisible by 10
    return sum_product % 10 == 0

@app.route('/')
def form():
    return render_template('input_data.html')

@app.route('/submit_form', methods=['POST'])
def handle_form():
    id_number = request.form.get('id')
    name = request.form.get('name')
    gender = request.form.get('gender')
    email = request.form.get('email')

    # Validate ID number
    if not validate_id(id_number):
        return "Invalid ID number", 400

    # Validate name (assuming it's alphabetic)
    if not re.match(r'^[A-Za-z\s]+$', name):
        return "Invalid name", 400

    # Validate gender
    if gender not in ['Male', 'Female']:
        return "Invalid gender", 400

    # Validate email
    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        return "Invalid email", 400

    return "All entries are valid", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)  # Listen on all available network interfaces and port 80

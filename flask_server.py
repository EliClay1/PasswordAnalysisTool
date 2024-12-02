from flask import Flask, render_template, request
import random

usable_symbols = "! @ # $ % ^ & * ( )".split()
usable_numbers = "1 2 3 4 5 6 7 8 9 0".split()
lowercase_index = "a b c d e f g h i j k l m n o p q r s t u v w x y z".split()
uppercase_index = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z".split()

def generate_password():
    return_password = ""
    compiled_password = [random.choice(usable_symbols) for i in range(random.randint(3, 6))]
    compiled_password += [random.choice(usable_numbers) for i in range(random.randint(5, 6))]
    compiled_password += [random.choice(uppercase_index) for i in range(random.randint(5, 7))]
    compiled_password += [random.choice(lowercase_index) for i in range(random.randint(4, 7))]
    random.shuffle(compiled_password)
    for char in compiled_password:
        return_password += char
    return return_password

def password_analysis(user_password):
    return_data = []
    grade = 100

    # Checks for spaces
    if " " in user_password:
        return_data.append("Password cannot have any spaces. Please try again.")

    # Checks length of password
    if len(user_password) <= 12:
        grade -= 10
        return_data.append("Password is too short.")
    elif len(user_password) <= 15:
        grade -= 5
        return_data.append("Password could be longer.")

    # Checks for symbol, number, and lettercase counts
    symbol_sum = 0
    number_sum = 0
    upper_sum = 0
    lower_sum = 0
    for character in user_password:
        if character in usable_symbols:
            symbol_sum += 1
        if character in usable_numbers:
            number_sum += 1
        if character in uppercase_index:
            upper_sum += 1
        if character in lowercase_index:
            lower_sum += 1
    if symbol_sum < 2:
        grade -= 10
        return_data.append("Password needs more special characters.")
    elif symbol_sum < 3:
        grade -= 5
        return_data.append("Password could use more special characters.")
    if number_sum <= 2:
        grade -= 10
        return_data.append("Password needs more numbers.")
    elif number_sum < 5:
        grade -= 5
        return_data.append("Password could use more numbers.")
    if upper_sum < 2:
        grade -= 5
        return_data.append("Password needs more uppercase letters.")
    if lower_sum < 2:
        grade -= 5
        return_data.append("Password needs more lowercase letters.")

    # TODO Brute Force Algorithm (Did not have enough time to complete)
    if not brute_force_check():
        grade -= 20
        flags.append("Brute Force")
        return_data.append("Password is weak compared to 10 Million common passwords.")

    if grade >= 95:
        feedback = "Your password is CRAZY strong!"
    elif grade >= 90:
        feedback = "You have a strong password!"
    elif grade >= 80:
        feedback = "Your password is pretty good"
    elif grade >= 70:
        feedback = "You have a okay password. Might want to strengthen it!"
    else:
        feedback = "That is a terrible password, do better."
    return grade, return_data, feedback

def brute_force_check():
    return True

########################################################################################################
"""FLASK SERVER"""
########################################################################################################

app = Flask(__name__)

@app.route("/")
def home():
    password = generate_password()
    return render_template("index.html", generated_password =password)  # Render the HTML form

@app.route("/analyze", methods=["POST"])
def analyze():
    password = request.form.get("password")
    if password:
        data = password_analysis(password)
        print(data)
        password = generate_password()
        return render_template("index.html", return_data=data[1], grade=data[0], feedback=data[2], generated_password=password)
    else:
        return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    password = generate_password()
    return render_template("index.html", generated_password=password)

if __name__ == "__main__":
    app.run(debug=False)

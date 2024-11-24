from fastapi import FastAPI
from pydantic import BaseModel
import math
from datetime import datetime

app = FastAPI()

# Unit Conversion
@app.get("/convert/units")
def convert_units(value: float, from_unit: str, to_unit: str):
    """
    Converts the given value from one unit to another.
    Handles length, weight, temperature, speed, volume, and area conversions.
    """
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    
    # Length conversion
    if from_unit == "meters" and to_unit == "feet":  # Meters to Feet
        return {"result": value * 3.28084}
    elif from_unit == "kilometers" and to_unit == "miles":  # Kilometers to Miles
        return {"result": value / 1.609}
    elif from_unit == "inches" and to_unit == "centimeters":  # Inches to Centimeters
        return {"result": value * 2.54}
    elif from_unit == "yards" and to_unit == "meters":  # Yards to Meters
        return {"result": value / 1.094}
    
    # Weight conversion
    if from_unit == "kilograms" and to_unit == "pounds":  # Kilograms to Pounds
        return {"result": value * 2.205}
    elif from_unit == "grams" and to_unit == "ounces":  # Grams to Ounces
        return {"result": value / 28.35}
    elif from_unit == "pounds" and to_unit == "kilograms":  # Pounds to Kilograms
        return {"result": value / 2.205}
    
    # Temperature conversion
    if from_unit == "celsius" and to_unit == "fahrenheit":  # Celsius to Fahrenheit
        return {"result": (value * 9/5) + 32}
    elif from_unit == "fahrenheit" and to_unit == "celsius":  # Fahrenheit to Celsius
        return {"result": (value - 32) * 5/9}
    elif from_unit == "kelvin" and to_unit == "celsius":  # Kelvin to Celsius
        return {"result": value - 273.15}
    elif from_unit == "celsius" and to_unit == "kelvin":  # Celsius to Kelvin
        return {"result": value + 273.15}
    elif from_unit == "fahrenheit" and to_unit == "kelvin":  # Fahrenheit to Kelvin
        return {"result": (value - 32) * 5/9 + 273.15}
    
    # Speed conversion
    if from_unit == "km/h" and to_unit == "mph":  # Kilometers per hour to Miles per hour
        return {"result": value / 1.609}
    elif from_unit == "m/s" and to_unit == "km/h":  # Meters per second to Kilometers per hour
        return {"result": value * 3.6}
    
    # Volume conversion
    if from_unit == "liters" and to_unit == "gallons":  # Liters to Gallons
        return {"result": value / 3.785}
    elif from_unit == "milliliters" and to_unit == "ounces":  # Milliliters to Ounces
        return {"result": value / 29.574}
    elif from_unit == "cubic meters" and to_unit == "liters":  # Cubic Meters to Liters
        return {"result": value * 1000}
    
    # Area conversion
    if from_unit == "square meters" and to_unit == "square feet":  # Square Meters to Square Feet
        return {"result": value * 10.764}
    elif from_unit == "acres" and to_unit == "square meters":  # Acres to Square Meters
        return {"result": value * 4046.86}
    
    return {"error": "Conversion not supported"}

# Text Processing
@app.get("/process/text/wordcount")
def word_count(text: str):  
    """
    Counts the number of words in the given text.
    Splits the text by spaces and counts the resulting list length.
    """
    word_count = len(text.split())
    return {"word_count": word_count}

@app.get("/process/text/charcount")
def char_count(text: str, include_spaces: bool = True):
    """
    Counts the number of characters in the text.
    Optionally excludes spaces from the count.
    """
    if include_spaces:
        char_count = len(text)  # Count all characters including spaces
    else:
        char_count = len(text.replace(" ", ""))  # Count characters excluding spaces
    return {"char_count": char_count}

@app.get("/process/text/reverse")
def reverse_text(text: str): 
    """
    Reverses the input text.
    """
    reversed_text = text[::-1]
    return {"reversed_text": reversed_text}

@app.get("/process/text/replace")
def replace_text(text: str, old_substring: str, new_substring: str): 
    """
    Replaces occurrences of old_substring with new_substring in the given text.
    """
    replaced_text = text.replace(old_substring, new_substring)
    return {"replaced_text": replaced_text}

@app.get("/process/text/capitalize")
def capitalize_text(text: str): 
    """
    Capitalizes the first letter of each word in the input text.
    """
    capitalized_text = text.title()  # Uses title case to capitalize each word
    return {"capitalized_text": capitalized_text}

@app.get("/process/text/length")
def text_length(text: str): 
    """
    Returns the length (number of characters) of the text.
    """
    return {"text_length": len(text)}

@app.get("/process/text/uppercase")
def to_uppercase(text: str): 
    """
    Converts all characters in the text to uppercase.
    """
    uppercase_text = text.upper()
    return {"uppercase_text": uppercase_text}

@app.get("/process/text/lowercase")
def to_lowercase(text: str): 
    """
    Converts all characters in the text to lowercase.
    """
    lowercase_text = text.lower()
    return {"lowercase_text": lowercase_text}

@app.get("/process/text/palindrome")
def is_palindrome(text: str): 
    """
    Checks if the text is a palindrome.
    """
    cleaned_text = ''.join(e for e in text if e.isalnum()).lower()
    if cleaned_text == cleaned_text[::-1]:
        return {"is_palindrome": True}
    return {"is_palindrome": False}

# Math Utility
@app.get("/math/addition")
def addition(a: float, b: float):
    """
    Adds two numbers a and b and returns the result.
    """
    result = a + b
    return {"result": result}

@app.get("/math/subtraction")
def subtraction(a: float, b: float):
    """
    Subtracts the number b from a and returns the result.
    """
    result = a - b
    return {"result": result}

@app.get("/math/multiplication")
def multiplication(a: float, b: float):
    """
    Multiplies two numbers a and b and returns the result.
    """
    result = a * b
    return {"result": result}

@app.get("/math/division")
def division(a: float, b: float):
    """
    Divides the number a by b and returns the result.
    Returns an error message if division by zero is attempted.
    """
    if b == 0:
        return {"error": "Cannot divide by zero"}
    result = a / b
    return {"result": result}

@app.get("/math/exponentiation")
def exponentiation(base: float, exponent: float):
    """
    Raises the base to the power of the exponent and returns the result.
    """
    result = math.pow(base, exponent)
    return {"result": result}

@app.get("/math/squareroot")
def square_root(value: float):
    """
    Returns the square root of the given value.
    Returns an error message if the value is negative.
    """
    if value < 0:
        return {"error": "Cannot calculate the square root of a negative number"}
    result = math.sqrt(value)
    return {"result": result}

@app.get("/math/factorial")
def factorial(value: int):
    """
    Returns the factorial of the given number.
    """
    if value < 0:
        return {"error": "Cannot calculate the factorial of a negative number"}
    result = math.factorial(value)
    return {"result": result}

@app.get("/math/logarithm")
def logarithm(value: float, base: float = 10):
    """
    Returns the logarithm of a given number with the specified base.
    """
    if value <= 0:
        return {"error": "Logarithm is not defined for non-positive numbers"}
    result = math.log(value, base)
    return {"result": result}

@app.get("/math/trigonometry")
def trigonometry(function: str, angle: float):
    """
    Returns the result of the trigonometric function (sin, cos, tan) for a given angle (in degrees).
    """
    radian = math.radians(angle)
    if function == "sin":
        result = math.sin(radian)
    elif function == "cos":
        result = math.cos(radian)
    elif function == "tan":
        result = math.tan(radian)
    else:
        return {"error": "Unsupported trigonometric function"}
    return {"result": result}

# Date and Time Utilities
@app.get("/datetime/format")
def format_datetime(date_string: str, format: str = "%Y-%m-%d"):
    """
    Formats a datetime string into the given format.
    The default format is YYYY-MM-DD.
    """
    try:
        date_obj = datetime.strptime(date_string, "%Y-%m-%d")  # default input format
    except ValueError:
        try:
            date_obj = datetime.strptime(date_string, "%d-%m-%Y")  # supporting alternative format
        except ValueError:
            return {"error": "Invalid date format"}
    formatted_date = date_obj.strftime(format)
    return {"formatted_date": formatted_date}

@app.get("/datetime/now")
def get_current_datetime():
    """
    Returns the current date and time in ISO format.
    """
    now = datetime.now()
    return {"current_datetime": now.isoformat()}

@app.get("/datetime/convert_timezone")
def convert_timezone(date_string: str, from_timezone: str, to_timezone: str):
    """
    Converts the input datetime from one timezone to another.
    """
    from pytz import timezone
    from_zone = timezone(from_timezone)
    to_zone = timezone(to_timezone)
    try:
        date_obj = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
        date_obj = from_zone.localize(date_obj)
        converted_date = date_obj.astimezone(to_zone)
        return {"converted_date": converted_date.strftime("%Y-%m-%d %H:%M:%S")}
    except Exception as e:
        return {"error": str(e)}

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

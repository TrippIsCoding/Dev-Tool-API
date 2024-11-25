from fastapi import FastAPI, Request, Response, HTTPException
from pydantic import BaseModel
import math
from datetime import datetime, timedelta
from typing import Optional
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

# Correct Middleware Implementation
class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        return response

# Add the middleware
app.add_middleware(CustomMiddleware)

# Unit Conversion Enhancements
@app.get("/convert/units")
def convert_units(value: float, from_unit: str, to_unit: str):
    conversions = {
        ("meters", "feet"): 3.28084,
        ("feet", "meters"): 1 / 3.28084,
        ("kilometers", "miles"): 1 / 1.609,
        ("miles", "kilometers"): 1.609,
        ("inches", "centimeters"): 2.54,
        ("centimeters", "inches"): 1 / 2.54,
        ("liters", "gallons"): 1 / 3.785,
        ("gallons", "liters"): 3.785,
        ("square meters", "square feet"): 10.764,
        ("square feet", "square meters"): 1 / 10.764,
    }

    key = (from_unit.lower(), to_unit.lower())
    if key in conversions:
        return {"result": value * conversions[key]}
    return {"error": f"Conversion from {from_unit} to {to_unit} is not supported."}

# Enhanced Text Processing
@app.get("/process/text/details")
def text_details(text: str):
    alphanumeric_count = sum(c.isalnum() for c in text)
    punctuation_count = sum(not c.isalnum() and not c.isspace() for c in text)
    whitespace_count = sum(c.isspace() for c in text)
    return {
        "length": len(text),
        "word_count": len(text.split()),
        "alphanumeric_count": alphanumeric_count,
        "punctuation_count": punctuation_count,
        "whitespace_count": whitespace_count,
    }

# Enhanced Math Utilities
@app.get("/math/trigonometry")
def trigonometry(function: str, angle: float, precision: Optional[int] = 4):
    radian = math.radians(angle)
    functions = {
        "sin": math.sin(radian),
        "cos": math.cos(radian),
        "tan": math.tan(radian),
        "sec": 1 / math.cos(radian) if math.cos(radian) != 0 else None,
        "csc": 1 / math.sin(radian) if math.sin(radian) != 0 else None,
        "cot": 1 / math.tan(radian) if math.tan(radian) != 0 else None,
    }

    if function not in functions:
        return {"error": f"Unsupported function '{function}'."}
    result = functions[function]
    if result is None:
        return {"error": f"Cannot compute '{function}' for angle {angle}."}
    return {"result": round(result, precision)}

# Date and Time Utilities
@app.get("/datetime/difference")
def date_difference(date1: str, date2: str, format: str = "%Y-%m-%d"):
    try:
        d1 = datetime.strptime(date1, format)
        d2 = datetime.strptime(date2, format)
        delta = d2 - d1
        return {"days_difference": abs(delta.days)}
    except ValueError as e:
        return {"error": str(e)}

@app.get("/datetime/convert_timezone")
def convert_timezone(date_string: str, from_timezone: str, to_timezone: str):
    try:
        from pytz import timezone
        from_zone = timezone(from_timezone)
        to_zone = timezone(to_timezone)
        date_obj = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
        localized_date = from_zone.localize(date_obj)
        converted_date = localized_date.astimezone(to_zone)
        return {"converted_date": converted_date.strftime("%Y-%m-%d %H:%M:%S")}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

from typing import Optional
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from collections import defaultdict
import math
from datetime import datetime, timedelta
import logging
import requests
from cachetools import TTLCache
from config import VALID_API_KEYS, RATE_LIMIT, RATE_LIMIT_WINDOW
import uvicorn
from pytz import UnknownTimeZoneError, timezone

# Initialize FastAPI app
app = FastAPI()

# Rate limiting storage
rate_limit_data = TTLCache(maxsize=1000, ttl=RATE_LIMIT_WINDOW)

# Setup logging
logging.basicConfig(filename="api_logs.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Currency Conversion Cache (TTL = 1 hour)
exchange_rate_cache = TTLCache(maxsize=1, ttl=3600)

def get_exchange_rate(from_currency, to_currency):
    """
    Fetch live exchange rates or use cached rates if available.
    """
    if exchange_rate_cache.get("rates"):
        rates = exchange_rate_cache["rates"]
    else:
        url = f"https://v6.exchangerate-api.com/v6/your_exchange_api_key/latest/{from_currency}"
        response = requests.get(url)
        if response.status_code != 200:
            raise HTTPException(
                status_code=500,
                detail="Failed to fetch exchange rates. Please try again later."
            )
        data = response.json()
        rates = data.get("conversion_rates", {})
        exchange_rate_cache["rates"] = rates

    if to_currency not in rates:
        raise HTTPException(
            status_code=400,
            detail=f"Conversion rate for {to_currency} not found."
        )
    return rates[to_currency]

@app.middleware("http")
async def api_key_and_rate_limiting_middleware(request: Request, call_next):
    client_ip = request.client.host
    now = datetime.now()

    # API Key Authentication
    api_key = request.headers.get("x-api-key")
    if not api_key or api_key not in VALID_API_KEYS:
        return JSONResponse(
            status_code=401, content={"error": "Unauthorized. Valid API key required."}
        )

    # Rate Limiting
    # Ensure there's a default empty list for new `client_ip`
    if client_ip not in rate_limit_data:
        rate_limit_data[client_ip] = []

    timestamps = rate_limit_data[client_ip]
    timestamps = [ts for ts in timestamps if now - ts < timedelta(seconds=RATE_LIMIT_WINDOW)]
    rate_limit_data[client_ip] = timestamps
    if len(timestamps) >= RATE_LIMIT:
        return JSONResponse(
            status_code=429, content={"error": "Rate limit exceeded. Try again later."}
        )
    rate_limit_data[client_ip].append(now)

    # Log request
    logging.info(f"Request from {client_ip} to {request.url.path}")
    response = await call_next(request)

    # Log response
    logging.info(f"Response to {client_ip} for {request.url.path}: {response.status_code}")
    return response


# Exception Handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"error": "Validation error", "details": exc.errors()},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "details": str(exc)},
    )

@app.get("/convert/currency")
def convert_currency(amount: float, from_currency: str, to_currency: str):
    """
    Convert an amount from one currency to another using live exchange rates.
    """
    try:
        rate = get_exchange_rate(from_currency.upper(), to_currency.upper())
        converted_amount = amount * rate
        return {
            "amount": amount,
            "from_currency": from_currency,
            "to_currency": to_currency,
            "converted_amount": round(converted_amount, 2),
            "rate": rate,
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        return {"error": str(e)}

@app.get("/convert/units")
def convert_units(value: float, from_unit: str, to_unit: str):
    conversions = {
        # Length Conversions
        ("meters", "feet"): 3.28084,
        ("feet", "meters"): 1 / 3.28084,
        ("kilometers", "miles"): 1 / 1.609,
        ("miles", "kilometers"): 1.609,
        ("inches", "centimeters"): 2.54,
        ("centimeters", "inches"): 1 / 2.54,
        ("yards", "meters"): 0.9144,
        ("meters", "yards"): 1 / 0.9144,
        ("miles", "yards"): 1760,
        ("yards", "miles"): 1 / 1760,
        
        # Area Conversions
        ("square meters", "square feet"): 10.764,
        ("square feet", "square meters"): 1 / 10.764,
        ("acres", "square meters"): 4046.86,
        ("square meters", "acres"): 1 / 4046.86,
        ("hectares", "square meters"): 10000,
        ("square meters", "hectares"): 1 / 10000,
        
        # Volume Conversions
        ("liters", "gallons"): 1 / 3.785,
        ("gallons", "liters"): 3.785,
        ("milliliters", "liters"): 0.001,
        ("liters", "milliliters"): 1000,
        ("cubic meters", "liters"): 1000,
        ("liters", "cubic meters"): 1 / 1000,
        
        # Weight/Mass Conversions
        ("kilograms", "pounds"): 2.20462,
        ("pounds", "kilograms"): 1 / 2.20462,
        ("grams", "ounces"): 1 / 28.3495,
        ("ounces", "grams"): 28.3495,
        ("tons", "kilograms"): 907.184,
        ("kilograms", "tons"): 1 / 907.184,
        
        # Speed Conversions
        ("kilometers/hour", "miles/hour"): 1 / 1.609,
        ("miles/hour", "kilometers/hour"): 1.609,
        ("meters/second", "kilometers/hour"): 3.6,
        ("kilometers/hour", "meters/second"): 1 / 3.6,
    }
    key = (from_unit.lower(), to_unit.lower())
    if key not in conversions:
        raise HTTPException(
            status_code=400,
            detail=f"Conversion from {from_unit} to {to_unit} is not supported."
        )
    result = value * conversions[key]
    return {"result": result}

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
        raise HTTPException(
            status_code=400,
            detail=f"Function '{function}' is not supported. Supported functions are: sin, cos, tan, sec, csc, cot."
        )
    result = functions[function]
    if result is None:
        return {"error": f"Cannot compute '{function}' for angle {angle}."}
    return {"result": round(result, precision)}

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
        from_zone = timezone(from_timezone)
        to_zone = timezone(to_timezone)
        date_obj = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
        localized_date = from_zone.localize(date_obj)
        converted_date = localized_date.astimezone(to_zone)
        return {"converted_date": converted_date.strftime("%Y-%m-%d %H:%M:%S")}
    except UnknownTimeZoneError:
        return {"error": "Invalid timezone provided."}
    except Exception as e:
        return {"error": f"Failed to convert timezone: {str(e)}"}

# Start the server if running this script
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

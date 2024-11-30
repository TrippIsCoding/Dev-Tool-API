Developer Tools API
A versatile API offering developer tools for various utilities like currency conversion, unit conversion, text processing, math functions, and datetime utilities. Built using FastAPI, it provides easy-to-use endpoints with comprehensive functionality.

Features
Currency Conversion: Convert amounts between currencies using live exchange rates.
Unit Conversion: Convert between length, area, volume, weight, and speed units.
Text Processing: Analyze text for length, word count, alphanumeric count, punctuation, and whitespace.
Math Utilities: Perform trigonometric calculations like sine, cosine, tangent, and more.
Datetime Utilities: Calculate date differences and convert timezones.

Live API
Base URL: https://dev-tool-api.onrender.com

Getting Started

Authentication
To use the API, include your API key in the headers of every request:

Header: x-api-key: YOUR_API_KEY

Requests per minute: 60
Rate Limit Window: 1 minute

Response Format
All responses are in JSON format. Errors include helpful messages and status codes.

Endpoints
Currency Conversion
Convert an amount between two currencies.

Endpoint: /convert/currency
Method: GET
Query Parameters:
amount: Amount to convert (float)
from_currency: Source currency (string, e.g., "USD")
to_currency: Target currency (string, e.g., "EUR")

Example Response:
{
  "amount": 100,
  "from_currency": "USD",
  "to_currency": "EUR",
  "converted_amount": 92.50,
  "rate": 0.925
}

Unit Conversion
Convert between units of length, area, volume, weight, and speed.

Endpoint: /convert/units
Method: GET
Query Parameters:
value: Value to convert (float)
from_unit: Source unit (string, e.g., "meters")
to_unit: Target unit (string, e.g., "feet")

Example Response:
{
  "result": 32.81
}

Text Processing
Analyze text for detailed statistics.

Endpoint: /process/text/details
Method: GET
Query Parameters:
text: Text to analyze (string)

Example Response:
{
  "length": 50,
  "word_count": 10,
  "alphanumeric_count": 40,
  "punctuation_count": 2,
  "whitespace_count": 8
}

Math Utilities: Trigonometry
Perform trigonometric calculations.

Endpoint: /math/trigonometry
Method: GET
Query Parameters:
function: Trigonometric function (string, e.g., "sin")
angle: Angle in degrees (float)
precision: Number of decimal places (optional, default is 4)

Example Response:
{
  "result": 0.7071
}

Datetime Utilities
Calculate Date Difference
Endpoint: /datetime/difference
Method: GET
Query Parameters:
date1: First date (string, e.g., "2023-01-01")
date2: Second date (string, e.g., "2023-01-10")
format: Date format (optional, default is "%Y-%m-%d")

Example Response:
{
  "days_difference": 9
}

Convert Timezone
Endpoint: /datetime/convert_timezone
Method: GET
Query Parameters:
date_string: Date and time (string, e.g., "2023-01-01 12:00:00")
from_timezone: Source timezone (string, e.g., "UTC")
to_timezone: Target timezone (string, e.g., "America/New_York")

Example Response:
{
  "converted_date": "2023-01-01 07:00:00"
}

Logging and Error Handling

Logging: All requests and responses are logged in api_logs.log.
Error Handling: Friendly error messages with HTTP status codes.


import requests

def make_api_request(params=None, headers=None, method='GET', data=None, json=None):
    api_url = "http://api.weatherstack.com/current?access_key=07a805ab78dbe6eba43095e7f4b415c6&query=Nairobi"
    
    try:
        response = requests.request(
            method=method,
            url=api_url,
            params=params,  
            headers=headers,
            data=data,
            json=json,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"API request failed: {e}")
        return None
    
def mock_api_request():
    return {
        "location": {
            "name": "Nairobi",
            "country": "Kenya",
            "region": "Nairobi Area",
            "lat": -1.286389,
            "lon": 36.817223,
            "timezone_id": "Africa/Nairobi",
            "localtime": "2023-10-01 12:00",
            "localtime_epoch": 1696156800,
            "utc_offset": 3
        },
        "current": {
            "observation_time": "12:00 PM",
            "temperature": 25,
            "weather_code": 113,
            "weather_icons": ["https://assets.weatherstack.com/images/wsymbols01_png_64/wsymbol_0008_sunny.png"],
            "weather_descriptions": ["Sunny"],
            "wind_speed": 15,
            "wind_degree": 180,
            "wind_dir": "S",
            "pressure": 1012,
            "precipitation": 0,
            "humidity": 50,
            "cloudcover": 20,
            "feelslike": 25,
            "uv_index": 6
        }
    }

# Example usage:
if __name__ == "__main__":
    result = make_api_request()
    print(result)
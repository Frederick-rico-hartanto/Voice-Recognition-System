import requests
from utils.speak import speak  # Assuming you have a custom speak function
from utils.api_keys import CURRENCY_API_KEY  # Your API key for currency conversion

# Function to convert currency using an API
def convert_currency(amount, from_currency, to_currency):
    url = f"https://v6.exchangerate-api.com/v6/{CURRENCY_API_KEY}/pair/{from_currency}/{to_currency}/{amount}"

    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code} from currency API")
            speak(f"Sorry, the currency conversion failed due to a network issue.")
            return None

        data = response.json()

        # Check for success in response
        if data.get("result") == "success":
            conversion_result = data.get("conversion_result")
            if conversion_result:
                speak(f"{amount} {from_currency} is equal to {conversion_result:.2f} {to_currency}")
                return conversion_result
            else:
                print(f"Error: No conversion result found in API response {data}")
                speak(f"Sorry, the currency conversion from {from_currency} to {to_currency} failed.")
                return None
        else:
            print(f"Error: API response did not indicate success: {data}")
            speak(f"Sorry, the currency conversion from {from_currency} to {to_currency} failed.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"RequestException during currency conversion: {e}")
        speak(f"Sorry, the currency conversion failed due to a network issue.")
        return None
    except Exception as e:
        print(f"Error during currency conversion: {e}")
        speak(f"Sorry, the currency conversion failed due to an error.")
        return None

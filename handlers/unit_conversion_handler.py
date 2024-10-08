from utils.speak import speak
import pint
import requests

# Initialize a unit registry for physical unit conversion
ureg = pint.UnitRegistry()


# Function to convert currency using an API (e.g., ExchangeRate-API or Open Exchange Rates)
def convert_currency(amount, from_currency, to_currency):
    API_KEY = "d4d54616e49ff713fac07c73"  # Replace with your actual API key
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{from_currency}/{to_currency}/{amount}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful (status code 200)
        data = response.json()

        # Check for valid response
        if "conversion_result" in data:
            conversion_result = data["conversion_result"]
            return conversion_result
        else:
            print(f"Error in response: {data}")
            return None

    except requests.exceptions.RequestException as e:
        # Handle any request-related errors
        print(f"Error during currency conversion: {e}")
        return None


# Main function to handle all unit conversions including currencies
def handle_unit_conversion(command):
    command = command.lower().replace("convert", "").replace("to", "").strip()

    try:
        words = command.split()
        value = float(words[0])  # The numeric value
        source_unit = words[1]  # The source unit (could be kg, g, USD, etc.)
        target_unit = words[-1]  # The target unit (could be g, kg, EUR, etc.)

        # Handle physical unit conversions (kg to g, liters to ml, etc.)
        if source_unit in ureg and target_unit in ureg:
            try:
                result = (value * ureg(source_unit)).to(target_unit)
                speak(f"{value} {source_unit} is equal to {result.magnitude:.2f} {target_unit}.")
            except pint.errors.DimensionalityError:
                speak(f"Cannot convert {source_unit} to {target_unit} directly.")
                print(f"Error during conversion: Cannot convert from '{source_unit}' to '{target_unit}'")

        # Handle currency conversions (USD to EUR, etc.)
        elif len(source_unit) == 3 and len(target_unit) == 3:  # Assuming 3-letter currency codes
            result = convert_currency(value, source_unit.upper(), target_unit.upper())
            if result:
                speak(f"{value} {source_unit.upper()} is equal to {result:.2f} {target_unit.upper()}.")
            else:
                speak("Sorry, I couldn't convert the currency.")

        else:
            speak("Unsupported units or currencies. Please check your input.")

    except Exception as e:
        speak("Sorry, I couldn't perform the conversion. Please try again with valid units.")
        print(f"Error during conversion: {e}")


# Example usage
if __name__ == "__main__":
    handle_unit_conversion("convert 5 kg to g")
    handle_unit_conversion("convert 10 liters to ml")
    handle_unit_conversion("convert 100 USD to EUR")

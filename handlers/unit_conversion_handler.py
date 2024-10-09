import pint  # For unit conversions
from utils.speak import speak  # Import your custom speak function

# Initialize Pint unit registry for unit conversions
unit_registry = pint.UnitRegistry()
Q_ = unit_registry.Quantity  # Shorthand for creating quantities

# Correct mappings for temperature units
temperature_units = {
    "fahrenheit": "degree_Fahrenheit",
    "celsius": "degree_Celsius",
    "kelvin": "kelvin"
}

# Function to convert units (including temperature conversions)
def convert_units(amount, from_unit, to_unit):
    try:
        # Map the input units to pint-compatible units
        from_unit_mapped = temperature_units.get(from_unit.lower(), from_unit)
        to_unit_mapped = temperature_units.get(to_unit.lower(), to_unit)

        # Print debug information to verify mappings
        print(f"Attempting to convert {amount} from '{from_unit_mapped}' to '{to_unit_mapped}'.")

        # Create a pint quantity
        quantity = Q_(amount, from_unit_mapped)

        # Convert directly using pint's to() method without explicit temperature context
        print(f"Converting {amount} from {from_unit_mapped} to {to_unit_mapped}...")
        converted_quantity = quantity.to(to_unit_mapped)

        return converted_quantity
    except pint.errors.DimensionalityError as e:
        print(f"Dimensionality Error: {e}")
        return None
    except Exception as e:
        print(f"Error during unit conversion: {e}")
        return None


# Main function to handle unit conversions
def handle_unit_conversion(command):
    try:
        if "convert" in command:
            parts = command.split()
            amount = float(parts[1])
            from_unit = parts[2]
            to_unit = parts[-1]

            # Handle unit conversions
            result = convert_units(amount, from_unit, to_unit)
            print(f"Unit conversion result: {result}")
            if result is not None:
                rounded_result = round(result.magnitude, 2)
                from_unit_formatted = from_unit.capitalize()
                to_unit_formatted = to_unit.capitalize()
                # Speak the result
                speak(f"{amount} {from_unit_formatted} is equal to {rounded_result} {to_unit_formatted}")
            else:
                speak(f"Sorry, I couldn't perform the unit conversion from {from_unit} to {to_unit}.")
        else:
            speak("Invalid command format. Use 'convert X from_unit to to_unit'.")
    except Exception as e:
        speak("Sorry, I couldn't perform the conversion. Please try again with valid inputs.")
        print(f"Error during conversion: {e}")


# Example usage
if __name__ == "__main__":
    handle_unit_conversion("convert 5 kg to g")  # Works
    handle_unit_conversion("convert 10 liters to mL")  # Works
    handle_unit_conversion("convert 100 centimeter**3 to decimeter**3")  # Volume conversion
    handle_unit_conversion("convert 100 centimeter**2 to meter**2")  # Area conversion
    handle_unit_conversion("convert 100 Fahrenheit to Celsius")  # Temperature conversion

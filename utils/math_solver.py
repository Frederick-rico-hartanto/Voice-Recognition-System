from utils.speak import speak

# Function to extract mathematical equation from the command
def extract_equation(command):
    math_related_phrases = ['solve', 'calculate', 'what is', 'find', 'evaluate', 'compute']
    for phrase in math_related_phrases:
        if phrase in command:
            return command.replace(phrase, "").strip()
    return command

# Function to solve mathematical equations using eval (for simple cases)
def solve_math_equation(equation):
    try:
        result = eval(equation)
        print(f"The result of {equation} is {result}")
        speak(f"The result of {equation} is {result}")
        return result
    except Exception as e:
        print(f"Error solving equation: {e}")
        speak("Error solving the equation")
        return None

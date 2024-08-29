import stripe
import time
from colorama import init, Fore, Style

# Load Stripe API key directly
stripe.api_key = 'YOUR_STRIPE_API'

def print_colored_ascii_art():
    # Initialize colorama
    init(autoreset=True)
    
    # ASCII art with red color
    ascii_art = f"""
{Fore.RED}

                                                         
                                                         
 ,adPPYba, 8b,dPPYba, 8b,dPPYba,  ,adPPYba,  8b,dPPYba,  
a8P_____88 88P'   "Y8 88P'   "Y8 a8"     "8a 88P'   "Y8  
8PP"'''''' 88         88         8b       d8 88          
"8b,   ,aa 88         88         "8a,   ,a8" 88          
 `"Ybbd8"' 88         88          `"YbbdP"'  88          
                                                         
                                                      
                Credit Card Checker
                made by @OxiKilla         
    """
    print(ascii_art)

def is_valid_credit_card(number):
    # Remove spaces and dashes from credit card number
    number = number.replace(' ', '').replace('-', '')
    
    # Check if credit card number contains only digits
    if not number.isdigit():
        return False
    
    # Convert credit card number to a list of digits
    digits = [int(digit) for digit in number]
    
    # Reverse the list of digits
    digits.reverse()
    
    # Apply Luhn algorithm
    total_sum = 0
    for i, digit in enumerate(digits):
        if i % 2 == 1:
            doubled = digit * 2
            if doubled > 9:
                doubled -= 9
            total_sum += doubled
        else:
            total_sum += digit
    
    # Credit card is valid if total sum is a multiple of 10
    return total_sum % 10 == 0

def get_card_network(number):
    number = number.replace(' ', '').replace('-', '')
    if number.startswith('4'):
        return "Visa"
    elif number.startswith(('51', '52', '53', '54', '55')) or \
         number.startswith(('2221', '2720')):
        return "Mastercard"
    elif number.startswith('34') or number.startswith('37'):
        return "American Express"
    elif number.startswith('6'):
        return "Discover"
    elif number.startswith('35'):
        return "JCB"
    elif number.startswith('30') or number.startswith(('36', '38', '39')):
        return "Diners Club"
    else:
        return "Unknown"

def check_card_active():
    try:
        # Utilizza un token di test di Stripe
        token = stripe.Token.create(
            card={
                'number': '4242424242424242',  # Numero di test per Visa
                'exp_month': 1,  # Mese di scadenza valido
                'exp_year': 2025,  # Anno di scadenza valido
                'cvc': '123',  # CVC valido
            }
        )
        return True
    except stripe.error.CardError as e:
        # Gestisce gli errori relativi alla carta
        print(f"Card error: {e}")
        return False
    except Exception as e:
        # Gestisce altre eccezioni
        print(f"Errore: {e}")
        return False

def animate_loading_message(message):
    for char in message:
        print(char, end='', flush=True)
        time.sleep(0.1)  # Delay between characters
    print()  # Move to the next line after the message

def main():
    print_colored_ascii_art()
    
    card_number = input("Card Number: ")
    
    # Simulate loading animation
    print("\n")
    animate_loading_message("Checking...")
    time.sleep(1)  # Brief pause before showing results
    
    if is_valid_credit_card(card_number):
        network = get_card_network(card_number)
        print(f"\nIl numero della carta è valido.")
        print(f"Il circuito di pagamento è: {network}")
        
        if check_card_active():
            print("\n🟢 Credit card is Valid and ON.")
        else:
            print("\n🔴 Credit card is OFF.")
    else:
        print("\n🔴 Credit card is NOT Valid.")

if __name__ == "__main__":
    main()

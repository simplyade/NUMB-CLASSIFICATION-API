from django.shortcuts import render

# Create your views here.
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)



def is_prime(number):
    if number <= 1:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False
    for d in range(3, int(number ** 0.5) + 1, 2):
        if number % d == 0:
            return False
    return True

def is_perfect(number: int) -> bool :
    """Check if a number is perfect."""
    return sum(i for i in range(1, number) if number % i == 0) == number

def is_armstrong(number):
    """Check if a number is an Armstrong number.""" 
    digits = str(number)
    power = len(digits)
    return sum(int(digit) ** power for digit in digits) == number


def get_fun_fact(number: int) -> str:
    """
    Fetches a fun fact about the given number from the Numbers API.
    
    Args:
        number (int): The number to fetch a fun fact for.
    
    Returns:
        str: A fun fact about the number or an appropriate error message.
    """
    url = f"http://numbersapi.com/{number}"
    
    try:
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            return response.text.strip()  # Strip extra whitespace
        
        return f"No fun fact available for {number} (HTTP {response.status_code})"
    
    except requests.exceptions.Timeout:
        return "Request timed out. The Numbers API took too long to respond."
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting fun fact: {e}")
        return "Error getting fun fact."

def number_properties(n):
    properties = []
    if n > 0:
        if is_armstrong(n):
            properties.append("armstrong")
    if n % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")
    return properties



@api_view(["GET"])
def classify_number(request):
    try :
        number = request.GET.get("number")

        ERROR_MESSAGE = {"number": "alphabet", "error": True}
        #reversed the conditional statement so it can catch the negative numbers
        if number:
            number = int(number)
            # properties = ["armstrong"] if is_armstrong(number) else []
            # properties.append("odd" if number % 2 != 0 else "even")
            properties = number_properties(number)#called the function

            return Response({
                "number": number,
                "is_prime": is_prime(number),
                "is_perfect": is_perfect(number),
                "properties": properties,
                # "digit_sum": sum(int(d) for d in str(number)),
                "digit_sum": sum(int(d) for d in str(abs(number))), # Fix for negative numbers
                "fun_fact": get_fun_fact(number),
            }, status=status.HTTP_200_OK)
        
    except ValueError:
            return Response(ERROR_MESSAGE, status=status.HTTP_400_BAD_REQUEST)
    return Response(ERROR_MESSAGE, status=status.HTTP_400_BAD_REQUEST)

   
from django.shortcuts import render
from django.http import JsonResponse
import requests

def main(request):
    return render(request, 'main.html')

def get_product_details(request, asin_code):
    api_key = 'F9F4F9B729B54C88BADCA4FE6B20748D'
    amazon_domain = 'amazon.com'
    url = f'https://api.rainforestapi.com/request'

    params = {
        'api_key': api_key,
        'type': 'product',
        'asin': asin_code,
        'amazon_domain': amazon_domain
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise exception for 4xx and 5xx status codes
        data = response.json()
        
        # Extract the relevant product details from the API response
        product_details = data.get('product', {})
        title = product_details.get('title', '')
        main_image_url = product_details.get('main_image', {}).get('link', '')

        # Construct the JSON response with the extracted product details
        response_data = {
            'title': title,
            'main_image_url': main_image_url
            # Include other product details here if needed
        }

        return JsonResponse({'product': response_data})

    except requests.exceptions.HTTPError as errh:
        return JsonResponse({'error': f"HTTP Error: {errh}"}, status=500)
    except requests.exceptions.RequestException as err:
        return JsonResponse({'error': f"Request Exception: {err}"}, status=500)
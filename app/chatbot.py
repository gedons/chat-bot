import json

# Load smartphone data from JSON file
with open('app/data.json') as f:
    smartphones = json.load(f)

# Global variables to store user selections
selected_brand = None
selected_model = None
available_phones = []
selected_phone_details = {}

def handle_chat(message):
    global selected_brand, selected_model, available_phones, selected_phone_details
    message = message.lower()
    response = ""

    try:
        if "brand" in message:
            brands = list(set(phone['brand'] for phone in smartphones))
            response = f"Welcome to our smartphone store! We have brands like {', '.join(brands)}. Which brand are you interested in?"

        elif any(brand.lower() in message for brand in list(set(phone['brand'] for phone in smartphones))):
            selected_brand = next((phone for phone in smartphones if phone['brand'].lower() in message), None)
            if selected_brand:
                models = list(set(model['name'] for model in selected_brand['models']))
                response = f"Great choice! Which model of {selected_brand['brand']} are you looking for?\n Models Available: \n{'\n '.join(models)}."
            else:
                available_brands = list(set(phone['brand'] for phone in smartphones))
                response = f"Sorry, we don't have {message.capitalize()} in our store. Here are the brands available: {', '.join(available_brands)}."

        elif selected_brand and any(model['name'].lower() in message for model in selected_brand['models']):
            selected_model = next((model for model in selected_brand['models'] if model['name'].lower() in message), None)
            if selected_model:
                colors = list(set(color['name'] for color in selected_model['colors']))
                response = f"Excellent! What color are you considering for the {selected_model['name']}?\n Colors Available: \n{'\n '.join(colors)}."
            else:
                available_models = list(set(model['name'] for model in selected_brand['models']))
                response = f"Sorry, we don't have that model in our store. Here are the available models: {', '.join(available_models)}."

        elif selected_brand and selected_model and any(color['name'].lower() in message for color in selected_model['colors']):
            chosen_color = next((color for color in selected_model['colors'] if color['name'].lower() in message), None)
            if chosen_color:
                # Filter phones by selected brand, model, and color
                available_phones = []
                for phone in smartphones:
                    if phone['brand'] == selected_brand['brand']:
                        for model in phone['models']:
                            if model['name'] == selected_model['name']:
                                for color in model['colors']:
                                    if color['name'].lower() == chosen_color['name'].lower():
                                        for price in color['prices']:
                                            available_phones.append((phone, model, color, price))
                                        break  # Exit the loop once the color is matched

                # List all available phones with the specified color
                if available_phones:
                    response = f"Perfect Choice! Here are the phones available in {chosen_color['name']} color:\n"
                    for idx, (phone, model, color, price) in enumerate(available_phones, start=1):
                        response += f"{idx}. {phone['brand']} \n {model['name']},\n Storage: {price['storage']},\n Price: ${price['price']}, \n Image: {price['imageUrl']}\n"
                    response += "Please select the number corresponding to your desired storage option."
                else:
                    response = f"Sorry, we don't have any phones available in {chosen_color['name']} color."

            else:
                available_colors = list(set(color['name'] for color in selected_model['colors']))
                response = f"Sorry, we don't have that color option. Here are the available colors: {', '.join(available_colors)}."

        elif any(storage_option.isdigit() for storage_option in message.split()) and "storage" not in message:
            selected_option = int(next((option for option in message.split() if option.isdigit()), None)) - 1
            if 0 <= selected_option < len(available_phones):
                selected_phone = available_phones[selected_option]
                selected_phone_details = {
                    'brand': selected_phone[0]['brand'],
                    'model': selected_phone[1]['name'],
                    'storage': selected_phone[3]['storage'],
                    'price': selected_phone[3]['price'],
                    'imageUrl': selected_phone[3]['imageUrl']
                }
                response = f"You've selected:\n{selected_phone_details['brand']} {selected_phone_details['model']},\n Storage: {selected_phone_details['storage']},\n Price: ${selected_phone_details['price']},\n Image: {selected_phone_details['imageUrl']}\n"
                response += "Please make the payment to proceed with your order.\n Payment Type:\n Card or Transfer"

            else:
                response = "Sorry, I didn't understand that selection. Please choose a valid storage option number."

        elif "card" in message:
            if selected_phone_details:
                response = f"Congratulations! You have successfully made payment with your card. Your {selected_phone_details['brand']} {selected_phone_details['model']} will be shipped to you. Thank you for using this channel👋"
                selected_phone_details = {}
            else:
                response = "I'm sorry, I didn't understand that. Please select a phone and storage option first."

        elif "transfer" in message:
            if selected_phone_details:
                response = f"Congratulations! You have successfully made payment via transfer.\n Your {selected_phone_details['brand']} {selected_phone_details['model']} will be shipped to you. Thank you for using this channel👋"
                selected_phone_details = {}
            else:
                response = "I'm sorry, I didn't understand that. Please select a phone and storage option first."

        else:
            response = "I'm sorry, I didn't understand that selection. Try Again!!!'."

    except Exception as e:
        response = f"An error occurred: {str(e)}"

    return response

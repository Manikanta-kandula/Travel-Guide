import boto3
import json
import os
import time
from dotenv import load_dotenv
from botocore.exceptions import ClientError  # Changed from ThrottlingException
from time import sleep

# Load environment variables from .env.local
load_dotenv(".env")

# Initialize Bedrock client
bedrock_runtime = boto3.client(
    'bedrock-runtime',
    region_name='us-east-1',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

def get_model_response(messages, max_retries=3):
    kwargs = {
        "modelId": "arn:aws:bedrock:us-east-1:390402541163:inference-profile/us.anthropic.claude-3-5-sonnet-20241022-v2:0",
        "contentType": "application/json",
        "accept": "application/json",
        "body": json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": messages
        })
    }
    
    for attempt in range(max_retries):
        try:
            response = bedrock_runtime.invoke_model(**kwargs)
            body = json.loads(response['body'].read())
            return body['content'][0]['text']
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'ThrottlingException':
                if attempt == max_retries - 1:
                    print("AI: I'm experiencing high traffic. Please try again in a moment.")
                    return "I'm experiencing high traffic. Please try again in a moment."
                wait_time = (attempt + 1) * 2  # Exponential backoff
                print(f"AI: Rate limit reached. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"An error occurred: {str(e)}")
                return "I encountered an error. Please try again."
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return "I encountered an error. Please try again."

def main():
    conversation = []
    
    # Initial instruction for the model
    initial_prompt = """You are a friendly and knowledgeable travel assistant designed to help users create personalized travel itineraries. Follow this structured conversational flow:

    Greet the user warmly and ask about their desired travel destination.

    Once they specify the location, ask follow-up questions to understand:
    • Their travel dates (arrival and departure)
    • Total budget for the trip
    • Travel preferences (adventure, culture, relaxation, food, etc.)
    • Number of travelers and any special considerations (family with kids, seniors, etc.)

    Ask about their accommodation preferences:
    • Preferred type (hotel, hostel, resort, vacation rental)
    • Desired location within the destination (city center, beachfront, etc.)
    • Budget range for accommodations

    Inquire about:
    • Transportation preferences (public transit, rental car, guided tours, etc.)
    • Must-see attractions or specific activities they're interested in
    • Any dietary restrictions or special requirements

    Once all information is gathered, summarize the user's inputs:
    • Destination
    • Travel dates
    • Total budget
    • Number of travelers
    • Accommodation preferences
    • Key interests and activities
    • Transportation needs

    Confirm the summary with the user and ask if they would like to modify anything.
    • If yes, update the plan accordingly
    • If no, proceed to generate the itinerary

    Generate a detailed day-by-day itinerary including:
    • Daily activities and attractions
    • Estimated costs for each activity
    • Recommended restaurants and dining experiences
    • Transportation details between locations
    • Buffer time for relaxation or spontaneous exploration
    • Local tips and cultural considerations
    • Weather-dependent backup plans

Ensure the itinerary:
• Respects the budget constraints
• Maintains a reasonable pace
• Includes location-specific practical tips
• Groups activities by geographic proximity
• Includes booking links or contact information where relevant"""

    # Add initial message to conversation
    initial_message = {
        "role": "user",
        "content": [{"type": "text", "text": initial_prompt}]
    }
    conversation.append(initial_message)
    
    # Get initial response with delay to avoid rate limiting
    print("AI: Initializing conversation...")
    time.sleep(1)  # Initial delay
    response = get_model_response(conversation)
    print(f"AI: {response}")
    
    while True:
        user_input = input("User: ")
        
        if user_input.lower() == 'exit':
            print("AI: Thank you for chatting! Goodbye!")
            break
            
        # Add user message to conversation
        user_message = {
            "role": "user",
            "content": [{"type": "text", "text": user_input}]
        }
        conversation.append(user_message)
        
        # Get model's response with built-in retry mechanism
        response = get_model_response(conversation)
        
        if response:  # Only add to conversation if we got a valid response
            assistant_message = {
                "role": "assistant",
                "content": [{"type": "text", "text": response}]
            }
            conversation.append(assistant_message)
            print(f"AI: {response}")
            
        # Add a small delay between interactions to avoid rate limiting
        time.sleep(1)

if __name__ == "__main__":
    main()



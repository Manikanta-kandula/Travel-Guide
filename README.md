# AI-Powered Travel Itinerary Planner

This is a **chat-based travel assistant application** that interacts with users to gather their preferences and generates a customized, day-by-day travel itinerary using **Amazon Bedrock's Claude 3.5 Sonnet model**. The assistant follows a structured conversational flow to ensure a tailored travel experience, including accommodation, transportation, and local recommendations.

## Features

- Interactive CLI-based chat experience
- Integrates with **Amazon Bedrock Runtime API**
- Automatically retries on throttling with exponential backoff
- Gathers detailed travel preferences through structured dialogue
- Summarizes user input and generates complete travel itineraries
- Includes practical tips, restaurant suggestions, and backup plans

## Technologies Used

- Python
- Boto3 (AWS SDK for Python)
- Amazon Bedrock (Claude 3.5 Sonnet)
- Dotenv for environment variable management

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/bedrock-travel-assistant.git
   cd bedrock-travel-assistant
   ```

2. **Create and configure the environment variables:**

   Create a `.env` file in the root directory with the following:
   ```
   AWS_ACCESS_KEY_ID=your-access-key-id
   AWS_SECRET_ACCESS_KEY=your-secret-access-key
   ```

3. **Install dependencies:**
   ```bash
   pip install boto3 python-dotenv
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

   The assistant will begin a conversation and guide the user through planning their ideal trip.

## Example Usage

```bash
AI: Hello! I'm your travel assistant. Where would you like to go?
User: Paris
AI: Great choice! What are your travel dates?
...
```

## File Structure

```
.
├── app.py                # Main Python script with chat interface logic
├── .env                  # Environment variable file (not checked into version control)
└── README.md             # Documentation
```

## Future Scope

- **Web Interface Integration:** Build a React or Next.js-based frontend to provide a seamless browser experience.
- **Voice Assistant Support:** Integrate with Amazon Lex or Alexa for voice-driven interactions.
- **Multi-language Support:** Enable itinerary planning in multiple languages.
- **Itinerary PDF Export:** Allow users to download their itinerary as a PDF file.
- **Map Integration:** Embed Google Maps or Mapbox for visualizing routes and nearby attractions.
- **Hotel/Flight Booking API Integration:** Add real-time booking links from providers like Expedia, Booking.com, or Skyscanner.
- **User Profiles:** Let users save and revisit previous itineraries.


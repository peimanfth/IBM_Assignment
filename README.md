# IBM Assignment

This assignment is a LangChain AI Agent that can perform web searches, look up information on Wikipedia, and retrieve weather conditions for a specified city. This agent is only made for the purpose of a take-home assignment for IBM and serves no other purpose.

## Prerequisites

- Python 3.8 or higher
- An OpenAI API key
- A SerpAPI API key (only limited to 100 requests for free version)
- An OpenWeather API key

## Setup

1. Clone the repository:

   ```sh
   git clone https://github.com/peimanfth/IBM_Assignment.git
   cd IBM_Assignment
   ```

2. Create a virtual environment and activate it:

   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. Set up your API keys:

   - Open the `config.py` file and replace the placeholder API keys with your actual API keys. You can also refer to my email for my own keys which will not be valid for long.
   - Alternatively, you can set the environment variables `OPENAI_API_KEY`, `SERPAPI_API_KEY`, and `OPENWEATHER_API_KEY` with your API keys.

## Running the Application

1. Run the main script:

   ```sh
   python assignment.py
   ```

2. Interact with the AI agent by typing your queries. Type `exit` or `quit` to stop the application.

## File Structure

- `config.py`: Configuration file for storing API keys.
- `assignment.py`: Main script that sets up and runs the LangChain AI agent.
- `requirements.txt`: List of required Python packages.

## Usage

The AI agent can perform the following tasks:

- **Wikipedia Lookup**: Look up information on Wikipedia using the `wikipedia` Python library.
- **Web Search**: Perform a general web search using SerpAPI (optional).
- **Weather Checker**: Retrieve current weather conditions for any city using the OpenWeather API.

## License

This project is licensed under the MIT License.

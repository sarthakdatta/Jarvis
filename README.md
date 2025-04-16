# Jarvis - Your Personal Assistant

## Description

Jarvis is a simple personal assistant built with Python, leveraging speech recognition, text-to-speech, and the power of large language models through Ollama. It listens for the activation word "Jarvis" and then responds to commands or questions, providing information and automating basic tasks.

## Features and Functionality

*   **Voice Activation:** Activates upon hearing the keyword "Jarvis".
*   **Web Browsing:** Opens specified websites (YouTube, Google, Gmail, Google Classroom) with voice commands.
*   **Weather Information:** Retrieves and speaks the current weather information for a specified city (defaults to Folsom).
*   **Conversational AI:**  Engages in conversations and answers questions using the `llama3.2` model through Ollama.
*   **Text-to-Speech:** Uses `pyttsx3` to speak responses.
*   **Multi-Turn Memory** Uses LangChain to store past conversations to make future responses more accurate

## Technology Stack

*   **Python:** The core programming language.
*   **Langchain:** For prompt engineering and memory.
*   **Ollama:** For running the `llama3.2` language model.
*   **Pyttsx3:** For text-to-speech functionality.
*   **SpeechRecognition:** For voice input.
*   **Requests:** For making HTTP requests to the OpenWeatherMap API.
*   **dotenv:** For loading environment variables.
*   **OpenWeatherMap API:** Used to retrieve weather data.

## Prerequisites

Before running Jarvis, ensure you have the following installed:

1.  **Python:** Python 3.6 or higher is required.

2.  **Python Packages:** Install the necessary Python packages using pip:

    ```bash
    pip install langchain_core langchain_ollama ollama pyttsx3 SpeechRecognition requests python-dotenv
    ```

3.  **Ollama:** Install Ollama from [https://ollama.com/](https://ollama.com/).

4.  **Ollama Model:** Download the `llama3.2` model.

    ```bash
    ollama pull llama3.2
    ```

5.  **OpenWeatherMap API Key:**
    *   Sign up for a free API key at [https://openweathermap.org/](https://openweathermap.org/).
    *   Set the `OPEN_WEATHER_API_KEY` environment variable.  You can do this by creating a `.env` file in the project directory:

        ```
        OPEN_WEATHER_API_KEY=YOUR_API_KEY
        ```

## Installation Instructions

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/sarthakdatta/Jarvis.git
    cd Jarvis
    ```

2.  **Install Dependencies:**

    ```bash
    pip install langchain_core langchain_ollama ollama pyttsx3 SpeechRecognition requests python-dotenv
    ```

3.  **Configure Environment Variables:**

    Create a `.env` file in the project directory and add your OpenWeatherMap API key:

    ```
    OPEN_WEATHER_API_KEY=YOUR_API_KEY
    ```

## Usage Guide

1.  **Run the Script:**

    ```bash
    python main.py
    ```

2.  **Activation:**  The script will start listening for the activation keyword "Jarvis".

3.  **Commands:** Once activated, you can give commands such as:

    *   "Open YouTube"
    *   "Open Google"
    *   "Open Gmail"
    *   "Open Google Classroom"
    *   "What's the weather" (or "Weather")
    *   "Stop"

4.  **Conversations:** If the command is not recognized, Jarvis will attempt to answer your question using the `llama3.2` model.

## API Documentation (OpenWeatherMap)

The weather functionality relies on the OpenWeatherMap API.

*   **Endpoint:** `http://api.openweathermap.org/data/2.5/weather`
*   **Parameters:**
    *   `q`: City name (e.g., `Folsom`)
    *   `appid`: Your API key
    *   `units`: Units of measurement (e.g., `imperial` for Fahrenheit)

## Contributing Guidelines

Contributions are welcome! To contribute:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes.
4.  Submit a pull request.

Please ensure your code follows PEP 8 guidelines and includes appropriate tests.

## License Information

No license specified.  Copyright belongs to the repository owner.

## Contact/Support Information

For questions or support, please contact:

Sarthak Datta - sarthakdatta.work@gmail.com

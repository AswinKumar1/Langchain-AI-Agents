# AI Voice Assistant using LangChain Agents and Speech Recognition

This project is a voice-controlled AI assistant powered by LangChain agents, Vosk for speech recognition, OpenAI for text generation and TTS, and SerpAPI for web searches. The assistant can fetch the current time, perform web searches, and create notes based on search results, with in-built test cases to ensure functionality.

## **Features**

- **Voice Commands:** Activate the assistant using voice commands.
- **Web Search:** Search the web using natural language and SerpAPI.
- **Note Creation:** Create and save notes using relevant web search results.
- **Audio Feedback:** Receive responses via speech.
- **In-built Testing:** Run unit tests directly from the command line.

## **Project Directory Structure**

```
voice-assistant/
├── notes/                  # Directory to store notes
├── main.py                 # Main application entry point
├── .env.example            # Example environment variables
├── requirements.txt        # List of dependencies
└── README.md               # Project overview and instructions
```

### **Installation**
1. Clone this repository:
   ```bash
   git clone https://github.com/AswinKumar1/voice-assistant.git
   cd voice-assistant
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Add your API keys to the `.env` file:
   ```
   SERPAPI_API_KEY=your_serpapi_api_key
   OPENAI_API_KEY=your_openai_api_key
   ```

## **Usage**

### **Running the Voice Assistant**
```bash
python main.py
```
The assistant will listen for commands and respond accordingly.

### **Running Tests**
To run the in-built unit tests, use:
```bash
python main.py test
```

## **Features Explained**
- **Time Tool:** Retrieve the current time using the command "What's the time?".
- **Web Search Tool:** Perform web searches with natural queries like "Tell me about AI".
- **Note-Making Tool:** Ask the assistant to create a note on a topic, and it will save the result in the `notes/` directory.
- **Audio Response:** The assistant will respond with spoken feedback using the PlayHT API.

---

## **Dependencies**
- `sounddevice` - For capturing audio input from the microphone.
- `vosk` - Offline speech recognition.
- `langchain` - LangChain for creating AI agents.
- `pydub` - Audio playback.
- `simpleaudio` - Stream and play audio responses.
- `serpapi` - Perform Google searches via SerpAPI.
- `unittest` - Built-in Python testing framework.


## **Unit Tests**
The following unit tests are integrated into the project:

1. **Test Time Tool:** Verifies the correct time format.
2. **Test Web Search Tool:** Ensures valid search results are returned.
3. **Test Note Creation:** Ensures a note is created correctly when requested.
4. **Test Note File Creation:** Checks that note files are stored in the correct directory.


## **Contributing**
Contributions are welcome! Feel free to submit a pull request or open an issue.


## **Future Enhancements**
- Add more tools (e.g., calendar meeting, send emails).
- Integrate streaming responses for faster feedback.
- Improve voice recognition accuracy.
- Break down the high level NLP into small tasks which can be carried out by the agents with available tools. 



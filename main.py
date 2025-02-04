import os
import queue
import sys
import sounddevice as sd
import unittest
from vosk import Model, KaldiRecognizer
import json
from langchain import hub
from langchain.agents import (
    AgentExecutor,
    create_react_agent,
)
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from serpapi import GoogleSearch
from datetime import datetime
from pydub import AudioSegment
import simpleaudio as sa

# Load environment variables
load_dotenv()
os.environ["SERPAPI_API_KEY"] = os.getenv("SERPAPI_API_KEY")

# Initialize the voice recognition model
q = queue.Queue()

# Ensure the 'notes' directory exists
if not os.path.exists("notes"):
    os.makedirs("notes")

# Simple tool to get the current time
def get_current_time(*args, **kwargs):
    now = datetime.now()
    return now.strftime("%I:%M %p")

# Web search using SerpAPI
def perform_web_search(query, **kwargs):
    api_key = os.getenv("SERPAPI_API_KEY")
    search = GoogleSearch({"q": query, "api_key": api_key})
    results = search.get_dict()
    if 'organic_results' in results and len(results['organic_results']) > 0:
        return results['organic_results'][0].get('snippet', 'No information found.')
    else:
        return "No relevant information found."

# Create a note based on a web search
def create_note_from_web_search(query, **kwargs):
    api_key = os.getenv("SERPAPI_API_KEY")
    search = GoogleSearch({"q": query, "api_key": api_key})
    results = search.get_dict()

    if 'organic_results' in results and len(results['organic_results']) > 0:
        snippet = results['organic_results'][0].get('snippet', 'No snippet available')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        note_filename = f"notes/{timestamp}_{query.replace(' ', '_')}.txt"
        with open(note_filename, 'w') as note_file:
            note_file.write(f"Query: {query}\nSnippet: {snippet}\n")
        return f"Note created successfully: {note_filename}"
    return "No relevant information found to create a note."

# List of tools available to the agent
tools = [
    Tool(name="Time", func=get_current_time, description="Get the current time"),
    Tool(name="WebSearch", func=perform_web_search, description="Perform a web search"),
    Tool(name="NoteMaking", func=create_note_from_web_search, description="Create a note from search results"),
]

# LangChain agent setup
prompt = hub.pull("hwchase17/react")
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
agent = create_react_agent(llm=llm, tools=tools, prompt=prompt, stop_sequence=True)
agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)

# Play audio
def play_audio(file_path):
    audio = AudioSegment.from_mp3(file_path)
    play_obj = sa.play_buffer(audio.raw_data, num_channels=audio.channels, bytes_per_sample=audio.sample_width, sample_rate=audio.frame_rate)
    play_obj.wait_done()

# Test cases using the unittest framework
class TestVoiceAssistant(unittest.TestCase):

    def test_get_current_time(self):
        result = get_current_time()
        self.assertIn("AM", result + "PM", "Time format should include AM or PM.")

    def test_web_search(self):
        result = perform_web_search("What is AI?")
        self.assertIsInstance(result, str, "Web search should return a string.")
        self.assertGreater(len(result), 0, "Web search result should not be empty.")

    def test_note_creation(self):
        query = "AI note"
        result = create_note_from_web_search(query)
        self.assertIn("Note created successfully", result, "Note creation should be successful.")

    def test_note_file_creation(self):
        query = "Test note"
        create_note_from_web_search(query)
        note_files = [f for f in os.listdir("notes") if f.startswith("Test_note")]
        self.assertGreater(len(note_files), 0, "A note file should be created for the query.")

# Main function to run the voice assistant or the tests
def main():
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Run tests if 'test' argument is provided
        unittest.main(argv=['first-arg-is-ignored'], exit=False)
    else:
        model = Model(lang="en-us")
        with sd.RawInputStream(samplerate=16000, blocksize=2000, dtype="int16", channels=1, callback=callback):
            print("#" * 80)
            print("Listening for commands...")
            print("#" * 80)

            rec = KaldiRecognizer(model, 16000)
            while True:
                try:
                    data = q.get(timeout=10)
                except queue.Empty:
                    print("No audio data received.")
                    continue

                if rec.AcceptWaveform(data):
                    result = rec.Result()
                    try:
                        recognized_text = json.loads(result)["text"].strip().lower()
                    except (json.JSONDecodeError, KeyError):
                        recognized_text = ""

                    if recognized_text:
                        print(f"Recognized command: {recognized_text}")
                        response = agent_executor.invoke({"input": recognized_text})
                        print("Response from LangChain agent:", response)

if __name__ == "__main__":
    main()

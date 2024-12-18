import streamlit as st
from pathlib import Path
from serper import serperquery
from main import GeminiModel
import os

gemini_api = os.getenv("Genai_api")
model_name = "gemini-1.5-flash"

GM = GeminiModel(gemini_api, model_name)

# Define the QueryProcessor class (from your original code)
class QueryProcessor:
    def __init__(self, query: str):
        self.query = query 
        self.serper_output = None
        self.formatted_prompt = None
        self.ai_response = None
        self.prompt_file = Path(r"D:\projects\Banarasia\prompt.txt")

    def get_serper_output(self):
        """Fetch search results from Serper API."""
        self.serper_output = serperquery(self.query)

    def load_and_format_prompt(self):
        """Load the prompt template and format it with query and search results."""
        if not self.prompt_file.is_file():
            raise FileNotFoundError(f"Prompt file not found at {self.prompt_file}")
        
        with self.prompt_file.open("r") as f: #opens the prompt file in read mode
            prompt_template = f.read()
        
        self.formatted_prompt = prompt_template.format(serper_output=self.serper_output, question=self.query) #formats the prompt with the search results and query

    def generate_ai_response(self):
        """Generate AI response using the Gemini model."""
        self.ai_response = GM.generate_content(self.formatted_prompt) #generates the response using the formatted_prompt

    def process_query(self):
        """Process the query by performing all necessary steps."""
        self.get_serper_output()
        self.load_and_format_prompt()
        self.generate_ai_response()

        return {
            "prompt": self.formatted_prompt,
            "search_results": self.serper_output,
            "ai_response": self.ai_response
        }

# Streamlit UI
st.title("AI Query Processor")
st.write("Enter a query to get search results and AI-generated responses.")

# Input field for user query
query = st.text_input("Enter your query:", placeholder="Type your question here (e.g., 'Tell me about Varanasi')")

# Process button
if st.button("Process Query"):
    if query.strip():  # Check if the query is not empty
        try:
            # Process the query using QueryProcessor
            query_processor = QueryProcessor(query)
            results = query_processor.process_query()

            # Display the results
            st.subheader("AI Response")
            st.write(results["ai_response"])
        except FileNotFoundError as e:
            st.error(f"Error: {e}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a valid query.")

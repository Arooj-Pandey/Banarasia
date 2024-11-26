from fastapi import FastAPI, HTTPException
import uvicorn
from pathlib import Path
from serper import serperquery
from main import GeminiModel
import streamlit as st

# Initialize FastAPI app_finallication
app_final = FastAPI()

class QueryProcessor:
    def __init__(self, query: str):
        self.query = query
        self.seggregated_query = GeminiModel.generate_content(f"You have to give me the keywords for this query: {query} only give the keywords grouped together in a sentence, which can be used for a google search, nothing else")
        self.serper_output = None
        self.formatted_prompt = None
        self.ai_response = None
        self.prompt_file = Path(r"D:\projects\Banarasia\prompt.txt")

    
    
    def get_serper_output(self):
        """Fetch search results from Serper API."""
        try:
            self.serper_output = serperquery(self.seggregated_query)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching search results: {e}")

    def load_and_format_prompt(self):
        """Load the prompt template and format it with query and search results."""
        if not self.prompt_file.is_file():
            raise FileNotFoundError(f"Prompt file not found at {self.prompt_file}")
        
        with self.prompt_file.open("r") as f: # Read the prompt template and prompt path assigned above in constructor to prompt_file
            prompt_template = f.read()
        
        self.formatted_prompt = prompt_template.format(serper_output=self.serper_output, question=self.query)

    def generate_ai_response(self):
        """Generate AI response using the Gemini model."""
        try:
            self.ai_response = GeminiModel.generate_content(self.formatted_prompt)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating AI response: {e}")

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

# Define a route to process queries
@app_final.get("/{query}")
def process_query(query: str):
    """
    Endpoint to process user queries.
    Args:
        query (str): User's query from the URL.
    Returns:
        dict: A response containing search results and AI-generated content.
    """
    try:
        query_processor = QueryProcessor(query)  # Instantiate the QueryProcessor class
        query_processor.process_query()  # Process the query
        return query_processor.process_query()  # Return the result
    except FileNotFoundError as e:
        # Handle missing prompt file error
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        # Handle other errors
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

# Run the FastAPI app_finallication with uvicorn
if __name__ == "__main__":
    uvicorn.run(app_final, host="127.0.0.1", port=8001)



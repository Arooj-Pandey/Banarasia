# Import necessary modules
from fastapi import FastAPI, HTTPException, Request
import uvicorn
#from pydantic import BaseModel
from pathlib import Path
from serper import serperquery
from main import generate_content

# Initialize FastAPI application
app = FastAPI()

# Define a route to process queries
@app.get("/{query}")
def process_query(query: str):
    """
    Endpoint to process user queries.
    Args:
        query (str): User's query from the URL.
    Returns:
        dict: A response containing search results and AI-generated content.
    """
    try:
        # Step 1: Get search results from Serper
        serper_output = serperquery(query)

        # Step 2: Format the prompt using a predefined template 
        prompt_file = Path(r"D:\projects\Banarasia\prompt.txt")
        if not prompt_file.is_file():
            raise FileNotFoundError(f"Prompt file not found at {prompt_file}")
        
        with prompt_file.open("r") as f:
            prompt_template = f.read()  # Read the prompt template

        # Format the template with search results and user query
        formatted_prompt = prompt_template.format(serper_output = serper_output, question = query)

        print(formatted_prompt)    
        # Step 3: Generate AI response using the Gemini model
        ai_response = gemini(formatted_prompt)

        # Step 4: Return both search results and the AI response
        print(ai_response)
        return {
            "prompt": formatted_prompt,
            "search_results": serper_output,
            "ai_response": ai_response
        }
    except FileNotFoundError as e:
        # Handle missing prompt file error
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        # Handle other errors
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


if __name__ == "__main__":
    # Run the FastAPI application with uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)





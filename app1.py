import json
from serper import serperquery, serper_img_query, serper_maps_query, serper_video_query
from main import GeminiModel
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
import uvicorn

app = FastAPI()

api_key= os.getenv("Genai_api")


GM = GeminiModel(api_key,"gemini-1.5-flash")

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

        serper_output = serperquery(query)  
        
        
        keyword_seggregation_prompt_file = Path(r"D:\projects\Banarasia\prompts\keyword_seggregation.txt")
        if not keyword_seggregation_prompt_file.is_file():
            raise FileNotFoundError(f"Prompt file not found at {keyword_seggregation_prompt_file}")
                
        with keyword_seggregation_prompt_file.open("r") as f:
            keyword_seggregation_prompt_template = f.read()
            formatted_prompt_for_keyword_seggregation = keyword_seggregation_prompt_template.format(serper_output = serper_output, question = query) #need serper output for input and relative keyword seperation
        #generates seggregated keywords  
            Seggregated_keywords = GM.generate_content(formatted_prompt_for_keyword_seggregation)


# Route Keywords to Respective APIs
        def route_keywords(keywords):
            results = {"Text": [], "Image": [], "YouTube Video": [], "Maps": []}
            
            for category, keyword_list in keywords.items():
                for keyword in keyword_list:
                    if category == "Text":
                        result = serperquery(keyword)
                    elif category == "Image":
                        result = serper_img_query(keyword)
                    elif category == "YouTube Video":
                        result = serper_video_query(keyword)
                    elif category == "Maps":
                        result = serper_maps_query(keyword)
                    else:
                        result = f"Unknown category: {category}"
                    results[category].append({keyword: result})
            
            return results

        # Simulated LLM interaction
        def interact_with_llm(user_query, results):
            """
            Passes results to the LLM along with the user query to generate a coherent response.
            """
            llm_input = {
                "user_query": user_query,
                "api_results": results
            }

            # Simulate LLM processing
            prompt = (
                f"You are an assistant that synthesizes information based on API results. "
                f"The user query is: '{user_query}'. Here are the results: {json.dumps(results, indent=2)}. "
                f"Reframe the results to provide a meaningful response."
            )
            response = GM.generate_content(prompt)  # Replace with actual LLM API call
            return response

        results = route_keywords(Seggregated_keywords)
        final_output = interact_with_llm(query, results)

        # Display final reframed output
        print(final_output)

    except FileNotFoundError as e:
        # Handle missing prompt file error
            raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        # Handle other errors
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

if __name__ == "__main__":
    # Run the FastAPI application with uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

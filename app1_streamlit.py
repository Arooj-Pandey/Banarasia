import json
import os
import streamlit as st
from pathlib import Path
from serper import serperquery, serper_img_query, serper_video_query, serper_maps_query
from main import GeminiModel

def route_keywords(keywords):
    """
    Route keywords to respective search APIs based on categories.
    
    Args:
        keywords (dict): Dictionary of keyword categories and their lists.
    
    Returns:
        dict: Search results for each category.
    """
    results = {"Text": [], "Image": [], "YouTube Video": [], "Maps": []}
    
    for category, keyword_list in keywords.items():
        for keyword in keyword_list:
            try:
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
            except Exception as e:
                st.error(f"Error searching {keyword} in {category}: {e}")
    
    return results

def interact_with_llm(user_query, results, gm):
    """
    Generate a coherent response using LLM based on search results.
    
    Args:
        user_query (str): Original user query
        results (dict): Search results from different sources
        gm (GeminiModel): Gemini language model instance
    
    Returns:
        str: Synthesized response from the LLM
    """
    # Prepare prompt for LLM
    prompt = (
        f"You are an assistant that synthesizes information based on API results. "
        f"The user query is: '{user_query}'. Here are the results: {json.dumps(results, indent=2)}. "
        f"Reframe the results to provide a meaningful response."
    )
    
    # Generate response using Gemini
    response = gm.generate_content(prompt)
    return response

def main():
    # Set page configuration
    st.set_page_config(page_title="Multi-Source Query Assistant", page_icon="🔍")
       
    # Title and description
    st.title("Multi-Source Query Assistant")
    st.write("Get comprehensive information from multiple sources!")
    
    # API Key input (with security)
    api_key= os.getenv("Genai_api")
    if not api_key:
        st.warning("Please set the Genai API key in environment variables or Streamlit secrets.")
        return
    
    # Initialize Gemini Model
    try:
        gm = GeminiModel(api_key, "gemini-1.5-flash")
    except Exception as e:
        st.error(f"Failed to initialize Gemini Model: {e}")
        return
    
    # User input
    query = st.text_input("Enter your query:", placeholder="What would you like to know?")
    
    if st.button("Search and Analyze") or query:
        if not query:
            st.warning("Please enter a query.")
            return
        
        try:
            # Load keyword segregation prompt
            keyword_seggregation_prompt_file = Path(r"D:\projects\Banarasia\prompts\keyword_seggregation.txt")
            if not keyword_seggregation_prompt_file.is_file():
                st.error(f"Prompt file not found at {keyword_seggregation_prompt_file}")
                return
            
            # Read and format prompt
            with keyword_seggregation_prompt_file.open("r") as f:
                keyword_seggregation_prompt_template = f.read()
            
            # Perform initial search
            serper_output = serperquery(query)
            
            # Format prompt for keyword segregation
            formatted_prompt_for_keyword_seggregation = keyword_seggregation_prompt_template.format(
                serper_output=serper_output, 
                question=query
            )
            
            # Generate segregated keywords
            seggregated_keywords = gm.generate_content(formatted_prompt_for_keyword_seggregation)
            
            # Route keywords and get results
            results = route_keywords(seggregated_keywords)
            
            # Generate final response
            final_output = interact_with_llm(query, results, gm)
            
            # Display results
            st.subheader("Search Results")
            
            # Expanders for different result categories
            with st.expander("Text Results"):
                st.json(results["Text"])
            
            with st.expander("Image Results"):
                st.json(results["Image"])
            
            with st.expander("Video Results"):
                st.json(results["YouTube Video"])
            
            with st.expander("Maps Results"):
                st.json(results["Maps"])
            
            # Display AI-generated summary
            st.subheader("AI-Generated Summary")
            st.write(final_output)
        
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
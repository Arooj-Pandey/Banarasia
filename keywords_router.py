from serper import serperquery, serper_img_query, serper_video_query, serper_maps_query

keyword_seggregation_prompt_file = r"D:\projects\Banarasia\prompts\keyword_seggregation.txt"

with keyword_seggregation_prompt_file.open("r") as f:
        prompt_template = f.read()  # Read the prompt template

        # Format the template with search results and user query
        formatted_prompt = Keyword_prompt_template.format(route_keywords()) 

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
    
    print(results)

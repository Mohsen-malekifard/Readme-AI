# A simple CLI tool to generate a README.md file using a large language model.
# This script is designed to be a starting point for a viral GitHub project.
# It uses Python's `argparse` for a simple command-line interface.

import argparse
import os
import sys
import json
import requests

def get_readme_from_llm(project_description, api_key):
    """
    Calls a large language model API to generate a README.md content.
    
    Args:
        project_description (str): A brief description of the project.
        api_key (str): The API key for the LLM service.

    Returns:
        str: The generated README.md content as a Markdown string, or an error message.
    """
    
    # API URL and model are set here.
    # For this example, a dummy API is used. You should replace this with a
    # real API, such as Google Gemini or OpenAI.
    API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent"
    
    # Prompt for the LLM
    prompt = f"""
    You are a professional GitHub project assistant. Your task is to generate a comprehensive and well-structured README.md file
    for a new software project. The README should be written in Markdown format and include the following sections:
    1.  A clear and catchy title.
    2.  A brief but engaging description.
    3.  A "Features" section using a bulleted list.
    4.  A "Getting Started" section with instructions for installation and usage.
    5.  A "Contributing" section.
    6.  A "License" section.

    Based on the following project description, please generate the README content.
    
    Project Description: "{project_description}"
    """
    
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key  # Use a header for API key, or as a query parameter
    }
    
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }
    
    try:
        response = requests.post(f"{API_URL}?key={api_key}", headers=headers, data=json.dumps(payload))
        response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)
        response_json = response.json()
        
        # Parse the JSON response to get the text content
        generated_text = response_json['candidates'][0]['content']['parts'][0]['text']
        return generated_text
        
    except requests.exceptions.RequestException as e:
        return f"Error connecting to the API: {e}"
    except (KeyError, IndexError) as e:
        return f"Error parsing API response: The response structure is invalid. {e}"

def main():
    """
    Main function to parse command-line arguments and run the script.
    """
    parser = argparse.ArgumentParser(
        description="Generates a README.md file using an AI model."
    )
    parser.add_argument(
        "description",
        type=str,
        help="A short, descriptive sentence about your project."
    )
    
    args = parser.parse_args()
    
    # Get API key from environment variable
    api_key = os.getenv("API_KEY")
    if not api_key:
        print("Error: API key not found. Please set the 'API_KEY' environment variable.")
        sys.exit(1)
    
    print("Generating README.md...")
    readme_content = get_readme_from_llm(args.description, api_key)
    print(readme_content)

if __name__ == "__main__":
    main()

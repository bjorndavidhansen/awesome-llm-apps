import streamlit as st
import logging
from scrapegraphai.graphs import OmniScraperGraph

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

st.title("Web Scraping AI Agent 🕵️‍♂️")
st.caption("This app allows you to scrape websites for text and images using OpenAI API")

openai_access_token = st.text_input("OpenAI API Key", type="password")

if openai_access_token:
    # Update model selection to include GPT-4o
    model = st.radio(
        "Select the model",
        ["openai/gpt-4", "openai/gpt-4o"],  # Include GPT-4o as an option
        index=1,  # Set GPT-4o as the default
        format_func=lambda x: "GPT-4" if x == "openai/gpt-4" else "GPT-4o (Recommended for image analysis)"
    )
    
    graph_config = {
        "llm": {
            "api_key": openai_access_token,
            "model": model,
        },
    }
    
    url = st.text_input("Enter the URL of the website you want to scrape")
    user_prompt = st.text_input("What specific data do you want to extract? (Include both text and image descriptions)")
    
    if url and user_prompt:
        logging.info("Starting scraping process...")
        omni_scraper_graph = OmniScraperGraph(
            prompt=user_prompt,
            source=url,
            config=graph_config
        )
        
        if st.button("Scrape"):
            try:
                logging.info(f"Scraping URL: {url} with prompt: '{user_prompt}' using model: {model}")
                result = omni_scraper_graph.run()
                logging.info("Scraping completed successfully.")
                st.json(result)
                
                if 'images' in result:
                    for img_url in result['images']:
                        logging.debug(f"Displaying scraped image: {img_url}")
                        st.image(img_url, caption="Scraped Image")
            except Exception as e:
                logging.error(f"An error occurred: {e}")
                if "image" in str(e).lower():
                    st.error(f"An error occurred while processing images: {e}")
                else:
                    st.error(f"An error occurred: {e}")
    else:
        logging.warning("URL or user prompt is missing.")
        st.warning("Please provide both the URL and the user prompt to proceed.")
else:
    logging.warning("OpenAI API key is missing.")
    st.warning("Please provide an OpenAI API key to use this app.")

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import pathlib
import json
import textwrap
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown
from myApi.models import ConversationHistory
from bs4 import BeautifulSoup
import spacy
import requests
# from palm.generators import GPT2Generator
import openai
# from langchain.agents.agent_types import AgentType
# from langchain_experimental.agents.agent_toolkits import create_csv_agent, create_pandas_dataframe_agent
# from langchain_openai import ChatOpenAI, OpenAI
# import pandas as pd


# generator = GPT2Generator(model="gpt2-medium")

def get_gemini_api_key():
    with open("/Users/manjushreemuralidhara/Masters/V_IndepenentS/VisuallyImpairedAssistantbackendMilestone/myApi/gemini.txt", "r") as f:
        return f.read().strip()

GOOGLE_API_KEY = get_gemini_api_key()
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')

def generate_gemini_reply(user_message):
    chat = model.start_chat(history=[])
    response = chat.send_message(user_message)
    return response.text

def scrape_url_content(current_page_url):
    url = current_page_url
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    navigation_elements = soup.find_all(["a", "input"])
    hierarchy = []
    current_parent = None

    for element in navigation_elements:
        if element.name == "a":  # If it's a link
            text = element.get_text().strip()
            url = element.get("href", "").strip()  
            
            link = {"Text": text, "URL": url, "Children": []}
            if current_parent:
                current_parent["Children"].append(link)
            else:
                hierarchy.append(link)
            current_parent = link
        elif element.name == "input":  
            label = element.get("aria-label", "").strip() 
            input_type = element.get("type", "").strip()  
            name = element.get("name", "").strip() 
            
            input_field = {"Label": label, "Type": input_type, "Name": name, "Children": []}
            
            if current_parent:
                current_parent["Children"].append(input_field)
        else:
            current_parent = None

    return hierarchy

@csrf_exempt
def gemini_chat(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        user_message = json_data.get('message', '')
        current_page_url = json_data.get('url', '')

        # Scrape content from the provided URL
        scraped_content = scrape_url_content(current_page_url)

        # Construct the prompt for Gemini
        # prompt = textwrap.dedent("""\
        # Serve as a guide for navigation, acknowledging user greetings if the user uses phrases like 'hi' or 'hello' and awaiting their next query. Utilize the extracted data from the Wayback Machine website to furnish navigation directives along with relevant links or URLs tied to each element.
        
        # Assist users in navigating the site pertaining to {}, strictly adhering to the information available and abstaining from adding any extra details. Ensure responses are solely based on the provided text data and refrain from any speculative additions.
        
        # Take into account different scenarios to offer precise guidance, relying solely on the scraped content from the Wayback Machine. Respond appropriately to the following types of user queries:
        
        # 1. *Greetings*: Respond to user greetings such as 'hi' or 'hello' by acknowledging them and awaiting their next query.
        
        # 2. *Navigation Queries*: Provide navigation guidance based on the provided scraped content. Users may ask questions like:
        # - 'Can you help me find [specific information] on the site?'
        # - 'Where can I find [specific page/section] on the site?'
        # - 'How do I navigate to [specific page/section] on the site?'
        
        # 3. *Other Queries*: If the user asks questions unrelated to navigation, politely redirect them back to navigation-related queries, encouraging them to explore the site further.
        # """.format(user_message))

        prompt = textwrap.dedent(f"""\
            The following is the scraped content from the provided URL:
            
            {scraped_content}
            
            Based on the scraped data, please answer the following question:
            
            User Query: "{user_message}"
            
            Response:
        """)


    # Append user message and scraped content to prompt
        prompt += f"user_message: {user_message}\nscraped_content: {scraped_content}"


        if user_message:
            # Generate Gemini's reply based on the prompt
            reply = generate_gemini_reply(prompt)
            return JsonResponse({'reply': reply})

        # if user_message:
        #     # Generate PaLM's reply based on the prompt
        #     reply = generator.generate(prompt, max_tokens=150)
        #     return JsonResponse({'reply': reply})
        # if user_message:
        #     # Generate reply using GPT-3
        #     response = openai.Completion.create(
        #         engine="davinci-codex:2022.09.29",
        #         prompt=prompt,
        #         max_tokens=150
        #     )
        #     reply = response.choices[0].text.strip()
        #     return JsonResponse({'reply': reply})


    return JsonResponse({'error': 'Invalid request'}, status=400)
























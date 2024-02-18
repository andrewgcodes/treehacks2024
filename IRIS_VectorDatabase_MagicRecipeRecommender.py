import csv
from langchain_iris import IRISVector
from langchain.docstore.document import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings, FastEmbedEmbeddings
import getpass
import os
import json
from dotenv import load_dotenv
load_dotenv(override=True)
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.fastembed import FastEmbedEmbeddings
from langchain_iris import IRISVector
import replicate
from replicate.client import Client


os.environ["OPENAI_API_KEY"] = #API KEY

csv_file_path = "1000shortrecipes.csv"

documents = []
with open(csv_file_path, mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        recipe_text = row[13]
        #print(recipe_text)
        documents.append(Document(page_content=recipe_text))

embeddings = OpenAIEmbeddings()

collection_name = 'recipes_collection2'
connection_string = "iris://SuperUser:SYS2@localhost:1972/USER"

db = IRISVector.from_documents(
    embedding=embeddings,
    documents=documents,
    collection_name=collection_name,
    connection_string=connection_string,
)

def generate_search_queries(user_query):
    prompt = f"I want to find some food that matches this description or would fit the vibe: {user_query}. Please come up with exactly three possible queries that could lead to recipes with a similar vibe to what I want. Use this format {{\"queries\": [\"query1\", \"query2\", \"query3\"]}}. Do not say ANYTHING else other than the JSON format. Your response should begin with {{\"queries\":"
    replicate = Client(api_token=#API)
    print("Getting response from Mistral-7b...")
    try:
        response = replicate.run(
            "mistralai/mistral-7b-instruct-v0.2",
            input={
                "debug": False,
                "top_k": 50,
                "top_p": 0.9,
                "prompt": prompt,
                "temperature": 0.6,
                "max_new_tokens": 128,
                "min_new_tokens": -1,
                "prompt_template": "<s>[INST] {prompt} [/INST] ",
                "repetition_penalty": 1.15
            },
        )

        content_str = ''.join(list(response)).replace(', ]', ']') 
        print(content_str)

        content = json.loads(content_str) 
        print("Generated Search Queries:", content)
        search_queries = content["queries"]

    except json.JSONDecodeError:
        print("Failed to decode JSON from GPT response.")
        search_queries = []
    except KeyError:
        print("JSON does not contain 'queries' key.")
        search_queries = []

    return search_queries

def main():
    user_query = input("Enter your query: ")
    search_queries = generate_search_queries(user_query)
    print(search_queries)
    
        
    for query in search_queries:
        print(f"Results for query: '{query}'")
        
        docs_with_score = db.similarity_search_with_score(query)
        
        for doc, score in docs_with_score:
            if len(doc.page_content) > 30:
                print("-" * 80)
                print(f"Score: {score}")
                print(doc.page_content)
                print("-" * 80)

if __name__ == "__main__":
    main()

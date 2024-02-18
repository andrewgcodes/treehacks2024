# Vision Mama!
TreeHacks 2024 project.
**Scroll down** for details.
![VisionMama Photo](https://github.com/andrewgcodes/treehacks2024/blob/main/visionmama-photo.png?raw=true)

## Vision OS App

## AI Agent Pipeline for Recipe Generation, Food Search, and Instacart Ordering
We built an endpoint that we hit from our Vision Pro and our Reflex site.
Basically what happens is we submit a user's desired food such as "banana soup". We pass that to our fine-tuned Mistral-7b LLM to generate a recipe. Then, we quickly use GPT-4-turbo to parse the recipe and extract the ingredients. Then we use the SERP API on each ingredient to find where it can be purchased nearby. We prioritize cheaper ingredients and use an algorithm to try to visit the least number of stores to buy all ingredients. Finally, we populate an Instacart Order API call to purchase the ingredients (simulated for now since we do not have actual partner access to Instacart's API)

## Pre-training:
We found a dataset online of 250,000 recipes. We preprocessed them and split and tokenized them for pretraining.
We used the GPT2 Byte Pair Encoding tokenizer.
We trained our **40M parameter LLM** using modified [nanogpt implementation](https://github.com/karpathy/nanoGPT)
We didn't have time to figure out how to deploy the LLM so we went with our fine-tuned Mistral-7b model (which also performed better).
More details on our devpost.

## Fine-tuning:
We **LORA fine-tuned Mistral-7b** using MonsterAPI's online platform: MonsterAPI.ai. (Thank you to the team for giving us free credits!)
Settings: one epoch, Lora R = 8, Lora Alpha = 16, Dropout = 0, Bias = none, Gradient accumulation steps = 32, Lr = 0.0002, warmup steps = 100

Before fine-tuning, we prepared **250k recipes** we got from online into a standard instruct format using this script: prepareRecipesForFinetuning.py
The format is:
You are an expert chef. You know about a lot of diverse cuisines. You write helpful tasty recipes.\n\n###Instruction: please think step by step and generate a detailed recipe for {prompt}\n\n###Response:{completion}

We also lowercased all prompts and completions.
We experimented with **fine-tuning using 10k, 50k, and 250k recipes.**
We observed that using more data led to lower loss, but at diminishing returns.
We deployed our fine-tuned Mistral-7b (250k examples) using MonsterAPI.ai
The script finetuned-mistral7b-monsterapi.py demonstrates how we call the fine-tuned model as well as process the output into a standardized format using regex and string processing methods.

## Reflex.dev Web Chat Agent
We used Reflex.dev, which is like React but entirely in Python, to create a simple chat interface to interact with our agent, because most people do not have a Vision Pro.
We run GPT-3.5-turbo that is prompt engineered to provide nutritional information to the user if they ask a question. However, if the user begins their chat message with "get me " and then an imaginary food, it **triggers our AI agent pipeline** which then calls our **fine-tuned Mistral-7b** to generate a recipe, **GPT-4-turbo** to process and extract ingredients from the recipe, and then **Google Search via SERP API** and a sophisticiated **multiobjective ranking algorithm** to identify the cheapest and best ingredients from the minimal number of stores, and finally populates **Instacart order API** calls.
We hosted it on reflex.dev which was easy. We just did reflex deploy and put in our env variable from the terminal! Thank you to reflex.

## InterSystems IRIS Vector Database for Semantic Recipe Discovery:
We used the early access version of the **IRIS Vector Database**, running it on a Mac with Docker.
We embedded 10,000 unique recipes from diverse cuisines using OpenAI's **text-ada-002 embedding**.
We stored the embeddings and the recipes in an IRIS Vector Database.
Then, we let the user input a "vibe", such as "cold rainy winter day".
We use Mistral-7b to generate three **Hypothetical Document Embedding** (HyDE) prompts in a structured format.
We then query the IRIS DB using the three Mistral-generated prompts.
The key here is that regular semantic search **does not** let you search by vibe effectively.
If you do semantic search on "cold rainy winter day", it is more likely to give you results that are related to cold or rain, rather than foods.
Our prompting encourages Mistral to understand teh vibe of your input and convert it to better HyDE prompts.
Real example:
User input: something for a chilly winter day
Generated Search Queries: {'queries': ['warming winter dishes recipes', 'comfort food recipes for cold days', 'hearty stews and soups for chilly weather']}

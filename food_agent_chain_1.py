import requests
import json

def generate_recipe(prompt):
    url = "https://f40e171a-ade7-40c5-913b-84db8e5fd1f8.monsterapi.ai/generate"
    api_auth_token = #AUTH TOKEN

    headers = {
        "Authorization": f"Bearer {api_auth_token}",
        "Content-Type": "application/json"
    }

    data = {
        "prompt": f"You are an expert chef. You know about a lot of diverse cuisines. You write helpful tasty recipes.\n\n###Instruction: please think step by step and generate a detailed recipe for {prompt}\n\n###Response:",
        "stream": False,
        "max_tokens": 256,
        "n": 1,
        "best_of": 1,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "repetition_penalty": 1,
        "temperature": 0.7,
        "top_p": 1,
        "top_k": -1,
        "min_p": 0,
        "use_beam_search": False,
        "length_penalty": 1,
        "early_stopping": False
    }

    response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)

    if response.status_code == 200:
        response_text = response.text
        start_str = "recipe name: "
        end_str = "token_counts"
        start_idx = response_text.find(start_str) + len(start_str)
        end_idx = response_text.find(end_str)
        recipe_text = response_text[start_idx:end_idx]
        recipe_text = recipe_text.replace("\\n", "\n").replace('\\"', '"')
        replaced_string = recipe_text.replace("\\\n", "\n")
        lines = replaced_string.split('\n')
        reversed_lines = list(reversed(lines))
        for line in reversed_lines:
            if any(char.isdigit() for char in line):
                index_to_remove = lines.index(line)
                lines = lines[:index_to_remove]
                break
        cleaned_text = '\n'.join(lines)
        final_string = cleaned_text.replace("\\\n", "\n")
        print(final_string)
        return final_string
    else:
        print(f"Error: {response.status_code}, Message: {response.text}")
        return "Error"

def handler(pd: "pipedream"):
    print(pd.steps["trigger"]["event"]["body"]["desiredFood"])
    result = generate_recipe(pd.steps["trigger"]["event"]["body"]["desiredFood"])
    return {"generatedRecipe": result}

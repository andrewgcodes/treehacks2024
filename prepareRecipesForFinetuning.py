import pandas as pd

file_path = 'RAW_recipes 2.csv'
data = pd.read_csv(file_path)

def safe_lower(s):
    if pd.isna(s):
        return ""
    return str(s).lower()

def format_recipe_lowercase(row):
    ingredients = eval(safe_lower(row['ingredients']))
    formatted_ingredients = '\n'.join([f"{idx+1}. {ingredient}" for idx, ingredient in enumerate(ingredients)])

    steps = eval(safe_lower(row['steps']))
    formatted_steps = '\n'.join([f"{idx+1}. {step}" for idx, step in enumerate(steps)])

    recipe_name = safe_lower(row['name'])
    
    description = safe_lower(row['description'])
    recipe = (f"here is your recipe!\n"
              f"recipe name: {recipe_name}\n"
              f"description: {description}\n"
              f"minutes to make: {row['minutes']}\n"
              f"ingredients:\n{formatted_ingredients}\n"
              f"steps:\n{formatted_steps}\n").replace("  ", " ")
    return recipe

data['recipe'] = data.apply(format_recipe_lowercase, axis=1)

def create_prompt(row):
    recipe_name = safe_lower(row['name'])
    prompt_text = f"please think step by step and generate a detailed recipe for {recipe_name.replace('  ', ' ')}"
    return prompt_text

data['prompt'] = data.apply(create_prompt, axis=1)

print(data.loc[0, 'recipe'])
print("\nPrompt Example:\n", data.loc[0, 'prompt'])

top_10000_shortest_recipes = data.sort_values(by='minutes').head(50000)

top_10000_shortest_recipes.head()

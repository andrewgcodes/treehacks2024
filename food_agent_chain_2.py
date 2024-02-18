import json
import serpapi

def handler(pd: "pipedream"):
    chat_content = pd.steps["chat"]["$return_value"]["choices"][0]["message"]["content"]
    ingredients = json.loads(chat_content)["ingredients"]
    
    results = []
    all_items = {} 
    store_coverage = {}  

    for ingredient in ingredients:
        query = f"{ingredient} near me"
        params = {
            "engine": "google",
            "q": query,
            "tbm": "shop",
            "location": "Stanford, California",
            "api_key": # SERP API KEY
        }
        
        search = serpapi.search(params)
        search_results = search.as_dict()
        shopping_results = search_results.get("shopping_results", [])
        
        sorted_results = sorted(shopping_results, key=lambda x: x.get("extracted_price", float('inf')))[:10]
        all_items[ingredient] = sorted_results
        
        for item in sorted_results:
            source = item["source"]
            if source not in store_coverage:
                store_coverage[source] = set()
            store_coverage[source].add(ingredient)

    ingredients_needed = set(ingredients)
    optimal_stores = {}
    while ingredients_needed:
        best_store = None
        best_coverage = set()
        for store, coverage in store_coverage.items():
            current_coverage = coverage & ingredients_needed
            if len(current_coverage) > len(best_coverage):
                best_store = store
                best_coverage = current_coverage
        
        if not best_store:
            break 
        
        optimal_stores[best_store] = list(best_coverage)
        ingredients_needed -= best_coverage

    shopping_lists = {}
    for store, ingredients_list in optimal_stores.items():
        shopping_lists[store] = []
        for ingredient in ingredients_list:
            for item in all_items[ingredient]:
                if item["source"] == store:
                    shopping_lists[store].append(item)
                    break  

    return {
        "shopping_lists": shopping_lists
    }

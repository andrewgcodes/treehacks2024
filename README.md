# Vision Mama!
TreeHacks 2024 project.
Scroll down for details.
![VisionMama Photo](https://github.com/andrewgcodes/treehacks2024/blob/main/visionmama-photo.png?raw=true)


Pre-training:
We found a dataset online of 250,000 recipes. We preprocessed them and split and tokenized them for pretraining.
We used the GPT2 Byte Pair Encoding tokenizer.
We trained our 40M parameter LLM using modified [nanogpt implementation](https://github.com/karpathy/nanoGPT)
We didn't have time to figure out how to deploy the LLM so we went with our fine-tuned Mistral-7b model (which also performed better).

Fine-tuning:
We LORA fine-tuned Mistral-7b using MonsterAPI's online platform: MonsterAPI.ai
Thank you to the team for giving us free credits!
We experimented with fine-tuning using 10k, 50k, and 250k recipes.
We observed that using more data led to lower loss, but at diminishing returns.
We deployed our fine-tuned Mistral-7b (250k examples) using MonsterAPI.ai
The script finetuned-mistral7b-monsterapi.py demonstrates how we call the fine-tuned model as well as process the output into a standardized format using regex and string processing methods.

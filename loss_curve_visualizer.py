import pandas as pd
import re
import matplotlib.pyplot as plt

path = 'recipeLoss2.txt'

iterations = []
losses = []

pattern = re.compile(r'iter (\d+): loss ([\d.]+),')

with open(path, 'r') as file:
    for line in file:
        match = pattern.search(line)
        if match:
            iterations.append(int(match.group(1)))
            losses.append(float(match.group(2)))

df = pd.DataFrame({
    'Iteration': iterations,
    'Loss': losses,
})

plt.figure(figsize=(12, 8))
plt.plot(df['Iteration'], df['Loss'], marker='o', linestyle='-', color='tab:red', markersize=1)
plt.title('Mini Recipe LM Training Loss Over Iterations')
plt.xlabel('Iteration')
plt.ylabel('Loss')
plt.grid(True)
plt.show()

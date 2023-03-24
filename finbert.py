import numpy as np
from transformers import BertTokenizer, BertForSequenceClassification

finbert = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone',num_labels=3)
tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')

labels = {0:'hold', 1:'buy',2:'sell'}

sent_val = list()

X = ["Abbott beats earnings, revenue expectations in Q4", "Activision Blizzard Inc. stock outperforms competitors despite losses on the day", "Adobe Inc. stock outperforms market on strong trading day",
     "Agilent Technologies Inc. stock rises Tuesday, still underperforms market", "Amazon.com Inc. stock underperforms Monday when compared to competitors", "Ameren Corp. stock underperforms Wednesday when compared to competitors despite daily gains",
     "American Water Works upgraded to neutral from underweight at J.P. Morgan", "AmerisourceBergen Corp. stock falls Friday, still outperforms market", "Amphenol Corp. Cl A stock outperforms competitors despite losses on the day"]
y = ["buy", "buy", "buy", "sell", "sell", "sell", "hold", "hold", "hold"]

for x in X:
    inputs = tokenizer(x, return_tensors="pt", padding=True)
    outputs = finbert(**inputs)[0]
   
    val = labels[np.argmax(outputs.detach().numpy())]
    print(x, '----', val)
    print('#######################################################')    
    sent_val.append(val)

from sklearn.metrics import accuracy_score
print(accuracy_score(y, sent_val))

# Read Text column from dataset.csv
import pandas as pd
df = pd.read_csv('dataset.csv')

# For each row in the Text column, get the sentiment value
sent_val = list()
for x in df['Text']:
    inputs = tokenizer(x, return_tensors="pt", padding=True)
    outputs = finbert(**inputs)[0]
    val = labels[np.argmax(outputs.detach().numpy())]
    print(f"{x} ---- {val}")
    sent_val.append(val)


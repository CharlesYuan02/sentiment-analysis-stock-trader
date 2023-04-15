import numpy as np
import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset, DataLoader
from transformers import AdamW
from transformers import BertTokenizer, BertForSequenceClassification

finbert = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone',num_labels=3)
tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')

labels = {0:'hold', 1:'buy',2:'sell'}

# Load dataset
df = pd.read_csv('finetune.csv')

# Convert labels to integers
df['label'] = df['label'].map({'hold': 0, 'buy': 1, 'sell': 2})

# Split dataset into train and validation sets
train_texts, val_texts, train_labels, val_labels = train_test_split(df['text'].values, df['label'].values, test_size=0.2)

# Tokenize inputs
train_encodings = tokenizer(list(train_texts), truncation=True, padding=True, max_length=256)
val_encodings = tokenizer(list(val_texts), truncation=True, padding=True, max_length=256)

# Convert to PyTorch tensors
train_dataset = torch.utils.data.TensorDataset(torch.tensor(train_encodings['input_ids']),
                                               torch.tensor(train_encodings['attention_mask']),
                                               torch.tensor(train_labels))
val_dataset = torch.utils.data.TensorDataset(torch.tensor(val_encodings['input_ids']),
                                             torch.tensor(val_encodings['attention_mask']),
                                             torch.tensor(val_labels))

# Create data loaders
train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=16, shuffle=True)
val_loader = torch.utils.data.DataLoader(val_dataset, batch_size=16, shuffle=False)

# Set device
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
finbert.to(device)

# Set optimizer and learning rate
optimizer = AdamW(finbert.parameters(), lr=2e-5)

# Fine-tune FinBERT
for epoch in range(5):
    # Train loop
    finbert.train()
    train_loss, train_acc = 0, 0
    for batch in train_loader:
        batch = tuple(t.to(device) for t in batch)
        inputs = {'input_ids': batch[0], 'attention_mask': batch[1], 'labels': batch[2]}
        outputs = finbert(**inputs)
        loss = outputs.loss
        train_loss += loss.item()
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        train_acc += (outputs.logits.argmax(dim=1) == batch[2]).sum().item()
    train_loss /= len(train_loader)
    train_acc /= len(train_loader.dataset)

    # Validation loop
    finbert.eval()
    val_loss, val_acc = 0, 0
    with torch.no_grad():
        for batch in val_loader:
            batch = tuple(t.to(device) for t in batch)
            inputs = {'input_ids': batch[0], 'attention_mask': batch[1], 'labels': batch[2]}
            outputs = finbert(**inputs)
            loss = outputs.loss
            val_loss += loss.item()
            val_acc += (outputs.logits.argmax(dim=1) == batch[2]).sum().item()
    val_loss /= len(val_loader)
    val_acc /= len(val_loader.dataset)

    print(f'Epoch {epoch + 1}: train_loss={train_loss:.4f}, train_acc={train_acc:.4f}, val_loss={val_loss:.4f}, val_acc={val_acc:.4f}')

# Save model
torch.save(finbert.state_dict(), 'finbert.pth')

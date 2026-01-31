import kagglehub
import pandas as pd
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from datasets import load_dataset
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader
from transformers import Trainer, TrainingArguments

# Importing model to be fine tuned
model = "roberta-base"
tokenizer = AutoTokenizer.from_pretrained(model)
model = AutoModelForSequenceClassification.from_pretrained(model, num_labels=2)

# CoLA dataset. Good for seeing if sentence makes sense
cola_path = kagglehub.dataset_download("krazy47/cola-the-corpus-of-linguistic-acceptability")

# wiki_sentence_order dataset. See if sentences are in right order
wiki_dataset = load_dataset("Fraser/wiki_sentences", split='train', streaming=True)

# Dataframes for the datasets
wiki_df = wiki_dataset.to_pandas()
cola_df = pd.read_csv(cola_path)

# Tokenize the dataframes
def tokenize_data(data):
    return tokenizer(data['text'], padding="max_length", truncation=True)

wiki_tokenized = wiki_df.map(tokenize_data, batched=True)
cola_tokenized = cola_df.map(tokenize_data, batched=True)

# Train test split
wiki_split = wiki_tokenized['train'].train_test_split(test_size=0.2)
cola_split = cola_tokenized['train'].train_test_split(test_size=0.2)

wiki_train = wiki_split['train']
wiki_test = wiki_split['test']
cola_train = cola_split['train']
cola_test = cola_split['test']

# DataLoaders to manage batches of data
wiki_train_dataloader = DataLoader(wiki_train, shuffle=True, batch_size=10)
wiki_test_dataloader = DataLoader(wiki_test, batch_size=10)

cola_train_dataloader = DataLoader(cola_train, shuffle=True, batch_size=10)
cola_test_dataloader = DataLoader(cola_test, batch_size=10)

# Arguments for training
training_parameters = TrainingArguments(
    output_dir='./results',
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch=10,
    per_device_eval_batch_size=10,
    num_train_epochs=5,
    weight_decay=0.01
)

# Training the models
wiki_trainer = Trainer(
    model=model,
    args = training_parameters,
    train_dataset=wiki_train,
    eval_dataset=wiki_test
)

cola_trainer = Trainer(
    model=model,
    arsg=training_parameters,
    train_dataset=cola_train,
    eval_dataset=cola_test
)

wiki_trainer.train()
cola_trainer.train()

print(f'wiki_trainer{wiki_trainer.evaluate()}')
print(f'cola_trainer{cola_trainer.evaluate()}')
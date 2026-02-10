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

# GLUE CoLA dataset
cola = load_dataset("glue", "cola", split="train")

# Tokenize the dataframes
def tokenize_data(data):
    return tokenizer(data['sentence'], padding="max_length", truncation=True)

def make_train_test():
    cola_split = cola['train'].train_test_split(test_size=0.2)
    tokenize = cola_split.map(tokenize_data(cola_split), batched=True)

    train = tokenize['train']
    test = tokenize['test']

    return train, test

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

def make_final_data():
    wiki_train, wiki_test = make_train_test()

    # Training the models
    wiki_trainer = Trainer(
        model=model,
        args = training_parameters,
        train_dataset=wiki_train,
        eval_dataset=wiki_test
    )

    wiki_trainer.train()

    return wiki_trainer

#print(f'wiki_trainer{wiki_trainer.evaluate()}')
#print(f'cola_trainer{cola_trainer.evaluate()}')
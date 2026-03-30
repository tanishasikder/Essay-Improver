import kagglehub
import pandas as pd
import torch
from transformers import (
    AutoModel, 
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorWithPadding)
from datasets import load_dataset
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader
from transformers import Trainer, TrainingArguments

# Importing model to be fine tuned
model = "roberta-base"
tokenizer = AutoTokenizer.from_pretrained(model)
model = AutoModel.from_pretrained(model, num_labels=2)

# GLUE CoLA dataset
cola = load_dataset("glue", "cola")

# Tokenize the dataframes
def tokenize_data(data):
    return tokenizer(data['sentence'], padding="max_length", truncation=True)

# Rename the label column. Required for HuggingFace
cola_dataset = cola.rename_column("label", "labels")

cola_train = cola_dataset["train"]
cola_test = cola_dataset["test"]

# Fit into train set then map into train test sets
tokenizer.fit(cola_train)
tokenized_cola_train = cola_train.map(tokenize_data, batched=True)
tokenized_cola_test = cola_test.map(tokenize_data, batched=True)

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
    train_dataset=tokenized_cola_train,
    eval_dataset=tokenized_cola_test
)

wiki_trainer.train()


#print(f'wiki_trainer{wiki_trainer.evaluate()}')
#print(f'cola_trainer{cola_trainer.evaluate()}')
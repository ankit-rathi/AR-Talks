# Python Hands-On Exercises for Data Analysts Transitioning to Data Engineering

## Purpose

These exercises are designed to build practical Python fluency, engineering thinking, and system design intuition using Google Colab.

---

# LEVEL 1 — PYTHON BASICS

## Exercise 1 — Variables & Data Types

```python
# Variables and basic calculations

total_records = 1000
failed_records = 25

passed_records = total_records - failed_records
pass_percentage = (passed_records / total_records) * 100
fail_percentage = (failed_records / total_records) * 100

print(f"Total Records: {total_records}")
print(f"Passed Records: {passed_records}")
print(f"Failed Records: {failed_records}")
print(f"Pass %: {pass_percentage:.2f}")
print(f"Fail %: {fail_percentage:.2f}")
```

---

## Exercise 2 — String Operations

```python
column_names = ["Customer Name", " Email Address ", "Phone Number"]

cleaned_columns = []

for col in column_names:
    clean_col = col.strip().lower().replace(" ", "_")
    cleaned_columns.append(clean_col)

print(cleaned_columns)
```

---

## Exercise 3 — Lists & Loops

```python
failed_columns = ["name", "email", "age"]

for column in failed_columns:
    print(f"Column {column} failed validation")
```

---

## Exercise 4 — Dictionaries

```python
rules = {
    "email": "not_null",
    "age": "range_check",
    "salary": "positive_check"
}

for column, rule in rules.items():
    print(f"Column: {column}, Rule: {rule}")
```

---

## Exercise 5 — Conditional Logic

```python
null_percentage = 12
threshold = 10

if null_percentage > threshold:
    print("Validation Failed")
else:
    print("Validation Passed")
```

---

## Exercise 6 — Functions

```python
def check_null(value):
    if value is None or value == "":
        return True
    return False

print(check_null(None))
print(check_null("John"))
```

---

## Exercise 7 — Default Arguments

```python
def validate(column_name, threshold=10):
    print(f"Validating {column_name} with threshold {threshold}")

validate("email")
validate("salary", 5)
```

---

## Exercise 8 — Lambda Functions

```python
values = [" Alice ", " Bob ", " Charlie "]

cleaned = list(map(lambda x: x.strip().lower(), values))

print(cleaned)
```

---

## Exercise 9 — List Comprehensions

```python
numbers = [1, 2, 3, 4, 5, 6]

odd_numbers = [n for n in numbers if n % 2 != 0]

print(odd_numbers)
```

---

## Exercise 10 — Exception Handling

```python
try:
    number = int("abc")
except ValueError:
    print("Invalid number provided")
finally:
    print("Execution Completed")
```

---

# LEVEL 2 — FILES & PANDAS

## Exercise 11 — Create and Read CSV

```python
import pandas as pd

sample_data = {
    "id": [1, 2, 3],
    "name": ["Alice", None, "John"],
    "email": ["alice@test.com", "bob@test.com", None]
}

# Create dataframe

df = pd.DataFrame(sample_data)

# Save CSV

df.to_csv("sample.csv", index=False)

# Read CSV

loaded_df = pd.read_csv("sample.csv")

print(loaded_df)
```

---

## Exercise 12 — Data Quality Summary

```python
import pandas as pd

sample_data = {
    "name": ["Alice", None, "John"],
    "email": ["alice@test.com", "bob@test.com", None]
}


df = pd.DataFrame(sample_data)

print("Total Records:", len(df))

for column in df.columns:
    null_count = df[column].isnull().sum()
    null_percentage = (null_count / len(df)) * 100

    print(f"Column: {column}")
    print(f"Null Count: {null_count}")
    print(f"Null %: {null_percentage:.2f}")
```

---

## Exercise 13 — JSON Handling

```python
import json

config = {
    "threshold": 10,
    "rules": {
        "email": "not_null"
    }
}

with open("config.json", "w") as file:
    json.dump(config, file)

with open("config.json", "r") as file:
    loaded_config = json.load(file)

print(loaded_config)
```

---

## Exercise 14 — File Handling

```python
with open("log.txt", "w") as file:
    file.write("Pipeline Started\n")

with open("log.txt", "r") as file:
    content = file.read()

print(content)
```

---

## Exercise 15 — Modularization

### utils.py

```python

def greet(name):
    return f"Hello {name}"
```

### main.py

```python
from utils import greet

print(greet("Team"))
```

---

# LEVEL 3 — OBJECT ORIENTED PYTHON

## Exercise 16 — Basic Class

```python
class DataValidator:

    def validate(self):
        print("Validation Running")

validator = DataValidator()
validator.validate()
```

---

## Exercise 17 — self Keyword

```python
class DataValidator:

    def set_name(self, name):
        self.name = name

    def display_name(self):
        print(self.name)

validator = DataValidator()
validator.set_name("DQ Engine")
validator.display_name()
```

---

## Exercise 18 — **init** Constructor

```python
class DataValidator:

    def __init__(self, dataset_name):
        self.dataset_name = dataset_name

    def display(self):
        print(f"Dataset: {self.dataset_name}")

validator = DataValidator("customer_data")
validator.display()
```

---

## Exercise 19 — Inheritance

```python
class BaseValidator:

    def log(self):
        print("Logging Validation")

class EmailValidator(BaseValidator):

    def validate(self):
        print("Email Validation Running")

validator = EmailValidator()
validator.log()
validator.validate()
```

---

## Exercise 20 — Private/Internal Methods

```python
class DataValidator:

    def _clean_data(self):
        print("Cleaning Data")

    def validate(self):
        self._clean_data()
        print("Validation Completed")

validator = DataValidator()
validator.validate()
```

---

# LEVEL 4 — DATA ENGINEERING THINKING

## Exercise 21 — Simple ETL Pipeline

```python
import pandas as pd

# Extract

data = {
    "name": [" Alice ", "Bob", "Bob"],
    "salary": [1000, 2000, 2000]
}


df = pd.DataFrame(data)

# Transform

df["name"] = df["name"].str.strip()
df = df.drop_duplicates()

# Load

df.to_csv("cleaned_output.csv", index=False)

print(df)
```

---

## Exercise 22 — Workflow Functions

```python

def extract():
    print("Extract Step")


def validate():
    print("Validate Step")


def transform():
    print("Transform Step")


def load():
    print("Load Step")

extract()
validate()
transform()
load()
```

---

## Exercise 23 — Logging

```python
import logging

logging.basicConfig(level=logging.INFO)

logging.info("Pipeline Started")
logging.info("Validation Running")
logging.info("Pipeline Completed")
```

---

## Exercise 24 — Dynamic Rule Engine

```python
import pandas as pd

sample_data = {
    "name": ["Alice", None],
    "email": ["alice@test.com", None]
}

rules = {
    "name": "not_null",
    "email": "not_null"
}


df = pd.DataFrame(sample_data)

for column, rule in rules.items():

    if rule == "not_null":
        failed = df[column].isnull().sum()

        print(f"{column} failed count: {failed}")
```

---

## Exercise 25 — Multi-file Processing

```python
files = ["file1.csv", "file2.csv", "file3.csv"]

for file in files:
    print(f"Processing {file}")
```

---

# LEVEL 5 — ADVANCED PRACTICAL PYTHON

## Exercise 26 — API Call

```python
import requests

url = "https://jsonplaceholder.typicode.com/users"

response = requests.get(url)

data = response.json()

print(data[0])
```

---

## Exercise 27 — Environment Variables

```python
import os

os.environ["DB_NAME"] = "customer_db"

print(os.getenv("DB_NAME"))
```

---

## Exercise 28 — Generators

```python

def generate_numbers():
    for i in range(5):
        yield i

numbers = generate_numbers()

for number in numbers:
    print(number)
```

---

## Exercise 29 — Type Hinting

```python

def validate(column: str) -> bool:
    print(f"Validating {column}")
    return True

validate("email")
```

---

## Exercise 30 — Mini Framework (Capstone)

```python
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

class RuleEngine:

    def __init__(self, dataframe, rules):
        self.dataframe = dataframe
        self.rules = rules

    def validate(self):

        for column, rule in self.rules.items():

            if rule == "not_null":
                failed = self.dataframe[column].isnull().sum()

                logging.info(f"{column} failed count: {failed}")

sample_data = {
    "name": ["Alice", None],
    "email": ["alice@test.com", None]
}

rules = {
    "name": "not_null",
    "email": "not_null"
}


df = pd.DataFrame(sample_data)

engine = RuleEngine(df, rules)
engine.validate()
```

---

# Recommended Team Operating Model

## Weekly Structure

### Monday

* Introduce concept
* Explain business relevance

### Tuesday–Wednesday

* Individual hands-on implementation

### Thursday

* Peer review + debugging session

### Friday

* Demo presentation
* Improvement discussion

---

# Recommended Progression

```text
Week 1 → Python basics
Week 2 → Functions & modularity
Week 3 → Pandas & files
Week 4 → OOP concepts
Week 5 → Data engineering patterns
Week 6 → Advanced Python & mini framework
```

---

# Final Goal

The objective is not just learning syntax.

The objective is helping analysts evolve from:

"people who execute scripts"

into:

"people who understand systems, design reusable logic, and think like engineers"

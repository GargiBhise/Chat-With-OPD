import torch
from transformers import PreTrainedTokenizerFast

# Load the model
model_path = "consolidated.00.pth"  # replace with your model file path
model = torch.load(model_path)

# Load the tokenizer
tokenizer = PreTrainedTokenizerFast(tokenizer_file="tokenizer.model")

# Load the parameters if necessary
import json
with open('params.json') as f:
    params = json.load(f)

def ask_model(query):
    # Preprocess the input. This includes:
    # 1. Tokenizing the input
    # 2. Converting the tokens to their corresponding IDs
    # 3. Adding batch dimension with unsqueeze
    inputs = tokenizer.encode(query, return_tensors='pt')

    # Generate a response from the model
    with torch.no_grad():
        outputs = model.generate(inputs, max_length=1000, do_sample=True)

    # Postprocess the output. This includes:
    # 1. Converting the output tensor to a list
    # 2. Decoding the tokens back into human-readable text
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return response

# Test the function
query = "What is the meaning of life?"
response = ask_model(query)
print(response)

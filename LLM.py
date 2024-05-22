# Import necessary libraries
import torch
import ollama
import os
from openai import OpenAI
import argparse
import json

# Define color codes for terminal output
PINK = '\033[95m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
NEON_GREEN = '\033[92m'
RESET_COLOR = '\033[0m'

# Function to open a file and return its contents as a string
def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

# Function to get relevant context from the vault based on user input
def get_relevant_context(rewritten_input, vault_embeddings, vault_content, top_k=3):
    # Check if the tensor has any elements
    if vault_embeddings.nelement() == 0:
        return []
    # Encode the rewritten input
    input_embedding = ollama.embeddings(model='mxbai-embed-large', prompt=rewritten_input)["embedding"]
    # Compute cosine similarity between the input and vault embeddings
    cos_scores = torch.cosine_similarity(torch.tensor(input_embedding).unsqueeze(0), vault_embeddings)
    # Adjust top_k if it's greater than the number of available scores
    top_k = min(top_k, len(cos_scores))
    # Sort the scores and get the top-k indices
    top_indices = torch.topk(cos_scores, k=top_k)[1].tolist()
    # Get the corresponding context from the vault
    relevant_context = [vault_content[idx].strip() for idx in top_indices]
    return relevant_context

# Function to rewrite the user's query by incorporating relevant context from the conversation history
def rewrite_query(user_input_json, conversation_history, ollama_model):
    # Load the user's query from the input JSON
    user_input = json.loads(user_input_json)["Query"]

    # Get the last two messages from the conversation history and join them into a single string
    context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history[-2:]])

    # Define the prompt for the Ollama API call
    prompt = f"""Rewrite the following query by incorporating relevant context from the conversation history.
    The rewritten query should:

    - Preserve the core intent and meaning of the original query
    - Expand and clarify the query to make it more specific and informative for retrieving relevant context
    - Avoid introducing new topics or queries that deviate from the original query
    - DONT EVER ANSWER the Original query, but instead focus on rephrasing and expanding it into a new query

    Return ONLY the rewritten query text, without any additional formatting or explanations.

    Conversation History:
    {context}

    Original query: [{user_input}]

    Rewritten query: 
    """

    # Generate the rewritten query using the Ollama API
    response = client.chat.completions.create(
        model=ollama_model,
        messages=[{"role": "system", "content": prompt}],
        max_tokens=200,
        n=1,
        temperature=0.1,
    )

    # Extract the rewritten query from the response
    rewritten_query = response.choices[0].message.content.strip()

    # Return the rewritten query as a JSON string
    return json.dumps({"Rewritten Query": rewritten_query})

# Function to handle the main chat interaction with the user
def ollama_chat(user_input, system_message, vault_embeddings, vault_content, ollama_model, conversation_history):
    # Append the user's input to the conversation history
    conversation_history.append({"role": "user", "content": user_input})

    # If there is more than one message in the conversation history, rewrite the user's query
    if len(conversation_history) > 1:
        # Prepare the JSON object for the query
        query_json = {
            "Query": user_input,
            "Rewritten Query": ""
        }
        # Call the rewrite_query function to rewrite the user's query
        rewritten_query_json = rewrite_query(json.dumps(query_json), conversation_history, ollama_model)
        # Parse the JSON response to get the rewritten query
        rewritten_query_data = json.loads(rewritten_query_json)
        rewritten_query = rewritten_query_data["Rewritten Query"]
        # Print the original and rewritten queries
        print(PINK + "Original Query: " + user_input + RESET_COLOR)
        print(PINK + "Rewritten Query: " + rewritten_query + RESET_COLOR)
    else:
        # If there's only one message in the conversation history, no need to rewrite the query
        rewritten_query = user_input

    # Get relevant context from the vault based on the rewritten query
    relevant_context = get_relevant_context(rewritten_query, vault_embeddings, vault_content)
    if relevant_context:
        # Join the relevant context into a single string
        context_str = "\n".join(relevant_context)
        print("Context Pulled from Documents: \n\n" + CYAN + context_str + RESET_COLOR)
    else:
        print(CYAN + "No relevant context found." + RESET_COLOR)

    # Add the relevant context to the user's input
    user_input_with_context = user_input
    if relevant_context:
        user_input_with_context = user_input + "\n\nRelevant Context:\n" + context_str

    # Update the last message in the conversation history with the user's input and relevant context
    conversation_history[-1]["content"] = user_input_with_context

    # Define the messages for the Ollama API call
    messages = [
        {"role": "system", "content": system_message},
        *conversation_history
    ]

    # Generate a response using the Ollama API
    response = client.chat.completions.create(
        model=ollama_model,
        messages=messages,
        max_tokens=2000,
    )

    # Append the assistant's response to the conversation history
    conversation_history.append({"role": "assistant", "content": response.choices[0].message.content})

    # Return the assistant's response
    return response.choices[0].message.content

# Parse command-line arguments
print(NEON_GREEN + "Parsing command-line arguments..." + RESET_COLOR)
# Create an ArgumentParser object
parser = argparse.ArgumentParser(description="Ollama Chat")
# Add an argument to the parser for the Ollama model
parser.add_argument("--model", default="llama3", help="Ollama model to use (default: llama3)")
# Parse the command-line arguments
args = parser.parse_args()

# Initialize the Ollama API client
print(NEON_GREEN + "Initializing Ollama API client..." + RESET_COLOR)
# Create an OpenAI client with the base URL and API key
client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='llama3'
)

# Load the vault content
print(NEON_GREEN + "Loading vault content..." + RESET_COLOR)
# Initialize an empty list for the vault content
vault_content = []
# Check if the vault file exists
if os.path.exists("vault.txt"):
    # Open the vault file and read its contents
    with open("vault.txt", "r", encoding='utf-8') as vault_file:
        vault_content = vault_file.readlines()

# Generate embeddings for the vault content using Ollama
print(NEON_GREEN + "Generating embeddings for the vault content..." + RESET_COLOR)
# Initialize an empty list for the vault embeddings
vault_embeddings = []
# For each line of content in the vault
for content in vault_content:
    # Generate an embedding for the line of content
    response = ollama.embeddings(model='mxbai-embed-large', prompt=content)
    # Add the embedding to the list of vault embeddings
    vault_embeddings.append(response["embedding"])

# Convert the embeddings to a tensor
print("Converting embeddings to tensor...")
# Convert the list of embeddings to a tensor
vault_embeddings_tensor = torch.tensor(vault_embeddings)
print("Embeddings for each line in the vault:")
print(vault_embeddings_tensor)

# Start the conversation loop
print("Starting conversation loop...")
# Initialize an empty list for the conversation history
conversation_history = []
# Define the system message
system_message = "You are a helpful assistant that is an expert at extracting the most useful information from a given text. Also bring in extra relevant infromation to the user query from outside the given context."

# Start an infinite loop
while True:
    # Prompt the user for input
    user_input = input(YELLOW + "Ask a query about your documents (or type 'quit' to exit): " + RESET_COLOR)
    # If the user types 'quit', break the loop
    if user_input.lower() == 'quit':
        break

    # Call the ollama_chat function to process the user's input and generate a response
    response = ollama_chat(user_input, system_message, vault_embeddings_tensor, vault_content, args.model,
                           conversation_history)
    # Print the response
    print(NEON_GREEN + "Response: \n\n" + response + RESET_COLOR)
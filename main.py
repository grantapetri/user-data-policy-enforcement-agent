import math
import os
import re

from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

POLICY_FILE = "policy.md"
TOP_K = 3

def required_env(name):
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Set the {name} environment variable.")
    return value

def load_policy_chunks():
    """Load each numbered policy rule as a separate chunk."""
    with open(POLICY_FILE, "r", encoding="utf-8") as file:
        policy = file.read()

    chunks = [
        chunk.strip()
        for chunk in re.split(r"(?=^### POLICY-\d+)", policy, flags=re.MULTILINE)
        if re.match(r"^### POLICY-\d+", chunk.strip())
    ]
    if not chunks:
        raise ValueError(f"No numbered policy rules found in {POLICY_FILE}.")
    return chunks

def cosine_similarity(left, right):
    dot_product = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(value * value for value in left))
    right_norm = math.sqrt(sum(value * value for value in right))
    if not left_norm or not right_norm:
        return 0.0
    return dot_product / (left_norm * right_norm)

def retrieve_relevant_policy(client, chunks, request, embedding_deployment):
    policy_response = client.embeddings.create(
        model=embedding_deployment,
        input=chunks,
    )
    request_response = client.embeddings.create(
        model=embedding_deployment,
        input=request,
    )

    policy_embeddings = sorted(policy_response.data, key=lambda item: item.index)
    if len(policy_embeddings) != len(chunks):
        raise RuntimeError("Embedding response did not include every policy rule.")
    request_embedding = request_response.data[0].embedding
    ranked_chunks = sorted(
        (
            (chunk, cosine_similarity(item.embedding, request_embedding))
            for chunk, item in zip(chunks, policy_embeddings)
        ),
        key=lambda item: item[1],
        reverse=True,
    )
    return ranked_chunks[:TOP_K]

def main():
    client = AzureOpenAI(
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview"),
        azure_endpoint=required_env("AZURE_OPENAI_ENDPOINT"),
        api_key=required_env("AZURE_OPENAI_API_KEY"),
    )
    chat_deployment = required_env("AZURE_OPENAI_CHAT_DEPLOYMENT")
    embedding_deployment = required_env("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")

    user = input("User: ").strip()
    role = input("Role: ").strip()
    requested_data = input("Data requested: ").strip()
    reason = input("Reason for request: ").strip()
    request = (
        f"User: {user}\n"
        f"Role: {role}\n"
        f"Data requested: {requested_data}\n"
        f"Reason: {reason}"
    )

    chunks = load_policy_chunks()
    relevant_policy = retrieve_relevant_policy(
        client, chunks, request, embedding_deployment
    )
    policy_context = "\n\n".join(
        f"{chunk}\nSimilarity: {score:.3f}" for chunk, score in relevant_policy
    )

    response = client.chat.completions.create(
        model=chat_deployment,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a data-access policy enforcement agent. Decide whether "
                    "the request is ALLOW, DENY, or PARTIAL using the supplied policy "
                    "rules. Do not assume permissions, valid business purpose, or "
                    "customer-level authorization that have not been established. "
                    "Return only JSON with decision, allowed_fields, denied_fields, "
                    "applicable_rules, and explanation. Never return customer data."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Request:\n{request}\n\n"
                    f"Most relevant policy rules:\n{policy_context}"
                ),
            },
        ],
    )
    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()

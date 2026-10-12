# user-data-policy-enforcement-agent
Enforce policy to ensure that data accesses are following policy

## Run

Set these environment variables to your Azure OpenAI endpoint, API key, and
deployment names. The embedding deployment must support embeddings.

```powershell
$env:AZURE_OPENAI_ENDPOINT = "https://<resource>.openai.azure.com/"
$env:AZURE_OPENAI_API_KEY = "<api-key>"
$env:AZURE_OPENAI_CHAT_DEPLOYMENT = "<chat-deployment>"
$env:AZURE_OPENAI_EMBEDDING_DEPLOYMENT = "<embedding-deployment>"
python main.py
```

The program asks for the user, role, requested data, and reason. It embeds the
numbered rules in `policy.md`, selects the three closest rules using cosine
similarity, and asks the chat deployment to return an ALLOW, DENY, or PARTIAL
decision as JSON.

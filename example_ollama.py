from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

# Inicjalizacja modelu z adresem serwera i modelem
model = ChatOllama(model="llama3.1:8b", base_url="http://10.8.0.1:8080")

# Wywołanie modelu
response = model.invoke([HumanMessage(content="Who is king julien?")])
print(response.content)

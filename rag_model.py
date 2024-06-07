# required libraries
import openai
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
loader = PyPDFLoader("data/Zivilgesetzbuch.pdf")
chunks = loader.load_and_split(text_splitter)

print("The chunk contains " + str(len(chunks[0].page_content)) + " characters")

# Load environment variables from .env file
load_dotenv()

# Access the API key using the variable name defined in the .env file
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI chat model
llm = ChatOpenAI(model_name="gpt-4o", temperature=0.8)

# Initialize the OpenAI embeddings model
embeddings = OpenAIEmbeddings()

# Variable for the Chroma database
chroma_db = None

if os.path.exists("civillaw_db"):
    print("Loading civillaw_db from disk...")
    chroma_db = Chroma(persist_directory="civillaw_db", embedding_function=embeddings)
else:
    chroma_db = Chroma.from_documents(documents=chunks,
                                      embedding=embeddings,
                                      persist_directory="civillaw_db",
                                      collection_name="lc_chroma")

# Function to generate and optimize prompts
def generate_prompt(context, question):
    role = "Du bist ein Anwalt, spezialisiert auf das Zivilgesetzbuch."
    task = "Erhalte die Frage des Mandanten und antworte mit einem lebensechten Alltagsbeispiel."
    steps = "Beantworte die Frage präzise und klar in nicht mehr als zwei Sätzen. Inkludiere relevante Abschnitte aus dem Schweizer Zivilgesetzbuch, falls zutreffend."
    example = "Frage: Ab wann ist eine Person erwachsen?\nAntwort: Art. 14 ZGB: Eine Person ist erwachsen, wenn sie das 18. Lebensjahr vollendet hat. Zum Beispiel, Anna wurde am 1. Januar 2004 geboren, sie wird daher am 1. Januar 2022 volljährig."
    format = "Bitte antworte immer auf Deutsch und beginne jede Antwort mit der Artikelbezeichnung des ZGBs, gefolgt von einem Doppelpunkt, bevor du die Antwort gibst. Starte die Antwort nie mit 'Anwalt:' oder ähnliches, sondern immer mit dem Artikel, wenn vorhanden."

    instruction = f"{role} {task} {steps} {format} {example}"
    optimized_prompt = f"{context}\nUser: {question}\n{instruction}"
    print("Generated Prompt:", optimized_prompt)  # Debug-Ausgabe
    return optimized_prompt

# Function to query the chain with optimized prompt
def query_chain(context, question):
    prompt = generate_prompt(context, question)
    response = chain.invoke(prompt)
    return response['result']

# Initialize the retrieval QA chain
chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=chroma_db.as_retriever())

# Example usage
def ask_question(conversation_history, question):
    context = "\n".join([f"Mandant: {msg['question']}\nAnwalt: {msg['answer']}" for msg in conversation_history])
    return query_chain(context, question)

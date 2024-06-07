# required libraries
import openai
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
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
    format = "Bitte antworte immer auf Deutsch und beginne jede Antwort mit der Artikelbezeichnung des ZGBs, gefolgt von einem Doppelpunkt, bevor du die Antwort gibst. Starte die Antwort nie mit 'Anwalt:' oder ähnliches, sondern immer mit dem Artikel, wenn vorhanden."
    
    # Few-shot examples
    examples = [
        "Frage: Ab wann ist eine Person erwachsen?\nAntwort: Art. 14 ZGB: Eine Person ist erwachsen, wenn sie das 18. Lebensjahr vollendet hat. Zum Beispiel, Anna wurde am 1. Januar 2004 geboren, sie wird daher am 1. Januar 2022 volljährig.",
        "Frage: Was passiert mit dem Eigentum eines Verstorbenen?\nAntwort: Art. 560 ZGB: Das Eigentum eines Verstorbenen geht direkt auf die Erben über. Beispielsweise, wenn Herr Müller stirbt, geht sein Haus sofort an seine Kinder über.",
        "Frage: Wann gilt eine Ehe als ungültig?\nAntwort: Art. 105 ZGB: Eine Ehe kann als ungültig erklärt werden, wenn einer der Ehegatten zur Zeit der Eheschließung geschäftsunfähig war. Zum Beispiel, wenn Max aufgrund eines schweren Unfalls nicht in der Lage war, Entscheidungen zu treffen, kann seine Ehe angefochten werden.",
        "Frage: Welche Rechte hat ein Mieter bei Mängeln an der Mietsache?\nAntwort: Art. 259a ZGB: Der Mieter kann eine Herabsetzung des Mietzinses verlangen, wenn ein erheblicher Mangel vorliegt. Zum Beispiel, wenn in Sarahs Wohnung die Heizung im Winter ausfällt, kann sie eine Mietzinsreduktion verlangen.",
        "Frage: Unter welchen Bedingungen kann ein Arbeitsvertrag gekündigt werden?\nAntwort: Art. 335 ZGB: Ein Arbeitsvertrag kann unter Einhaltung der vertraglich vereinbarten Kündigungsfrist gekündigt werden. Beispielsweise, wenn Peter eine Kündigungsfrist von drei Monaten hat, kann sein Arbeitgeber ihm unter Einhaltung dieser Frist kündigen.",
        "Frage: Wer ist verantwortlich für den Unterhalt eines Kindes?\nAntwort: Art. 276 ZGB: Die Eltern sind verpflichtet, für den Unterhalt des Kindes zu sorgen. Zum Beispiel, wenn Maria und Tom sich scheiden lassen, müssen beide weiterhin für die Kosten des Kindes aufkommen.",
        "Frage: Wann verjährt eine Forderung aus einem Kaufvertrag?\nAntwort: Art. 127 ZGB: Forderungen aus Kaufverträgen verjähren in fünf Jahren. Zum Beispiel, wenn Paul im Januar 2020 ein Auto verkauft hat und der Käufer nicht bezahlt hat, verjährt die Forderung im Januar 2025.",
        "Frage: Unter welchen Umständen kann ein Testament angefochten werden?\nAntwort: Art. 519 ZGB: Ein Testament kann angefochten werden, wenn der Erblasser beim Verfassen nicht urteilsfähig war. Beispielsweise, wenn Lisa unter dem Einfluss von Medikamenten stand und nicht klar denken konnte, könnte ihr Testament angefochten werden.",
        "Frage: Was sind die Voraussetzungen für die Adoption eines Kindes?\nAntwort: Art. 264 ZGB: Zur Adoption ist die Zustimmung des Kindes und der leiblichen Eltern erforderlich. Zum Beispiel, wenn Max und Julia ein Kind adoptieren wollen, müssen sowohl das Kind als auch seine leiblichen Eltern der Adoption zustimmen."
    ]
    
    instruction = f"{role} {task} {steps} {format}"
    examples_text = "\n\n".join(examples)
    optimized_prompt = f"{context}\n{examples_text}\nFrage: {question}\n{instruction}"
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

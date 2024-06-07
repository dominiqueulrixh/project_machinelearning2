# required libraries
import openai
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=300)
loader = PyPDFLoader("data/Zivilgesetzbuch.pdf")
chunks = loader.load_and_split(text_splitter)

print("The chunk contains " + str(len(chunks[0].page_content)) + " characters")

# Load environment variables from .env file
load_dotenv()

# Access the API key using the variable name defined in the .env file
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI chat model
llm = ChatOpenAI(model_name="gpt-4o", temperature=0.3)

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
    role = "You are a lawyer specializing in the Civil Code."
    task = "Answer civil law questions. Answer in the same language as the question is formulated. If the question is general, provide a brief description of your skills or knowledge."
    steps = "Start with the article reference. Answer the question. Add a real-life example."
    format = "Begin each answer with the article designation of the Civil Code if available, followed by a colon. Answer in no more than three sentences."

    # Few-shot examples
    examples = [
        "Question: From when is a person considered an adult?\nAnswer: Art. 14 ZGB: A person is considered an adult when they have reached the age of 18. For example, Anna was born on January 1, 2004, so she will be an adult on January 1, 2022.",
        "Question: What happens to the property of a deceased person?\nAnswer: Art. 560 ZGB: The property of a deceased person passes directly to the heirs. For example, when Mr. Müller dies, his house immediately goes to his children.",
        "Question: When is a marriage considered invalid?\nAnswer: Art. 105 ZGB: A marriage can be declared invalid if one of the spouses was incapacitated at the time of the marriage. For example, if Max was unable to make decisions due to a severe accident, his marriage can be contested.",
        "Question: What rights does a tenant have regarding defects in the rental property?\nAnswer: Art. 259a ZGB: The tenant can request a reduction in rent if there is a significant defect. For example, if the heating fails in Sarah's apartment during winter, she can request a rent reduction.",
        "Question: Under what conditions can an employment contract be terminated?\nAnswer: Art. 335 ZGB: An employment contract can be terminated by observing the contractually agreed notice period. For example, if Peter has a notice period of three months, his employer can terminate his contract by observing this notice period.",
        "Question: Who is responsible for the maintenance of a child?\nAnswer: Art. 276 ZGB: Parents are obligated to provide for the maintenance of the child. For example, if Maria and Tom divorce, both must continue to cover the costs for the child.",
        "Question: When does a claim from a sales contract expire?\nAnswer: Art. 127 ZGB: Claims from sales contracts expire in five years. For example, if Paul sold a car in January 2020 and the buyer did not pay, the claim expires in January 2025.",
        "Question: Under what circumstances can a will be contested?\nAnswer: Art. 519 ZGB: A will can be contested if the testator was not competent when drafting it. For example, if Lisa was under the influence of medication and could not think clearly, her will could be contested.",
        "Question: What are the requirements for adopting a child?\nAnswer: Art. 264 ZGB: Adoption requires the consent of the child and the biological parents. For example, if Max and Julia want to adopt a child, both the child and the biological parents must consent to the adoption."
    ]

    instruction = f"{role}\n{task}\n{steps}\n{format}"
    examples_text = "\n\n".join(examples)
    optimized_prompt = f"{context}\n\n{examples_text}\n\nQuestion: {question}\n\n{instruction}"
    print("Generated Prompt:", optimized_prompt)  # Debug-Ausgabe
    return optimized_prompt

# Function to query the chain with optimized prompt
def query_chain(context, question):
    if question.strip() == "":
        return "Please ask me something about the civil code."
        
    prompt = generate_prompt(context, question)
    response = chain.invoke(prompt)

    if prompt in response['result']:
        print("Irrelevant answer detected, retrying.")
        response['result'] = "It seems that your question was not specific enough. I specialize in the Swiss Civil Code and can answer questions on various legal topics such as marriage, inheritance law, tenancy law, and more."
    
    return response['result']

# Initialize the retrieval QA chain
chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=chroma_db.as_retriever())

# Example usage
def ask_question(conversation_history, question):
    context = "\n".join([f"Mandant: {msg['question']}\Boby: {msg['answer']}" for msg in conversation_history])
    return query_chain(context, question)
# import os is used to enter the huggingface api token such that 
# we dont have to do it everytime manually
import os
os.environ["HUGGINGFACEHUB_API_TOKEN"] = ""

#The below snippet helps us to import structured pdf file data for our tasks
from langchain.document_loaders import PyPDFDirectoryLoader
import pypdf

def load_docs(directory):
    for filename in os.listdir(directory):
        # Loads PDF files available in a directory with pypdf
        if filename.endswith('.pdf'):
            return load_docspdf(directory)
        # Passing the directory to the 'load_docs' function
        elif filename.endswith('.xlsx'):
            return load_docsexcel(directory)
        else:
            print(f"Unsupported file format: {filename}")

def load_docspdf(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.pdf'):
            loader = PyPDFDirectoryLoader(directory)
            documents = loader.load()
    return documents

#Assigning the data inside the pdf to our variable here
# Passing the directory to the 'load_docs' function
directory = '/workspaces/SEN-Bosco-Branch/data'
documents = load_docs(directory)

len(documents)

#This function will split the documents into chunks
from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_docs(documents, chunk_size=3000, chunk_overlap=20):
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
  docs = text_splitter.split_documents(documents)
  return docs

docs = split_docs(documents)

# The embedding model
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
embeddings = FastEmbedEmbeddings()

#Store and Index vector space
from langchain.vectorstores import FAISS
db = FAISS.from_documents(docs, embeddings)


# LLM Q&A Code
from langchain_community.llms import HuggingFaceHub
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
question = "What is ADHD?"
template = """Question: {question}
Answer: Let's think step by step."""
prompt = PromptTemplate(template=template, input_variables=["question"])
# llm = OpenAI()
# chain = load_qa_chain(llm, chain_type="stuff")
repo_id = "google/flan-t5-xxl"  # See https://huggingface.co/models?pipeline_tag=text-generation&sort=downloads for some other options
llm = HuggingFaceHub(
    repo_id=repo_id, model_kwargs={"temperature": 0.5, "max_length": 64}
)
llm_chain = LLMChain(prompt=prompt, llm=llm)

# This function will transform the question that we raise into input text to search relevant docs
def get_text():
    input_text = st.text_input("Parent: ", key = input)
    return input_text

#This function will help us in fetching the top k relevent documents from our vector store - Pinecone
def get_similiar_docs(query, k=2):
    similar_docs = db.similarity_search(query, k=k)
    return similar_docs

# This function will help us get the answer from the relevant docs matching input text
def get_answer(query):
  relevant_docs = get_similiar_docs(query)
  print(relevant_docs)
  response = llm_chain.run(input_documents=relevant_docs, question=query)
  return response

# the Main function that allows us to time how long it takes for
# answer generation
import time
if __name__ == "__main__":
    result = 0
    queries = ["What is ADHD?","What are the symptoms of ADHD?", "How is ADHD diagnosed?","What causes ADHD?", "How is ADHD treated?"]
    for query in queries:
        query_start = time.time()
        response = get_answer(query)
        query_end = time.time()
        duration = query_end-query_start
        result += duration
    print("_____")
    print("Time taken is:")
    print(f"{result} seconds")
    print("_____")

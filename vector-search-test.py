import os
from dotenv import load_dotenv
load_dotenv(".env")

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import DeepLake
from langchain.document_loaders import TextLoader
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain

embeddings = OpenAIEmbeddings(disallowed_special=())


root_dir = "./test-app/src"
# root_dir = "./superset/superset-frontend"
# root_dir = '/mnt/nvme0n1p3/Work/langchain/langchain'
db = None

try :
    db = FAISS.load_local(root_dir, embeddings)
except:
    print("Local DB not found")

    docs = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        print(dirnames)
        for file in filenames:
            # if file.endswith(".js") or file.endswith(".css") or file.endswith(".ts") or file.endswith(".tsx") or file.endswith(".jsx"):
            if file.endswith(".py"):
                try:
                    loader = TextLoader(os.path.join(dirpath, file), encoding="utf-8")
                    docs.extend(loader.load_and_split())
                except Exception as e:
                    pass
    print(f"Total docs found : {len(docs)}")


    print("Starting chunking...")
    text_splitter = CharacterTextSplitter(chunk_size=4000, chunk_overlap=0)
    texts = text_splitter.split_documents(docs)

    print("Creating db...")
    db = FAISS.from_documents(texts, embeddings)

    print("Saving db...")
    db.save_local(root_dir)


question1 = "What does the click me button do?"
docs = db.similarity_search(question1)
print("Similarity search below:-----")
print(docs[0].page_content)
print("--"*30)
print(docs[0].metadata)

filePath, fileContents = docs[0].metadata, docs[0].page_content

print(filePath or fileContents)
print((filePath or fileContents) is None)

if filePath is None or fileContents is None:

    print("Was unable to perform given task, maybe try again with full context of the task")




# retriever = db.as_retriever()
# model = ChatOpenAI(model_name="gpt-3.5-turbo")  # switch to 'gpt-4'
# model = ChatOpenAI(model_name="gpt-3.5-turbo-16k")  # switch to 'gpt-4'
# qa = ConversationalRetrievalChain.from_llm(model, retriever=retriever)


# # question1 = "When we call the from_llm method of ConversationalRetrievalChain class, which methods are executed and in what order?"
# question1 = "What does the 'Parsing LLM output produced both a final answer and a parse-able action' error mean? and how can I fix it"
# chat_history = []
# result = qa({"question": question1, "chat_history": chat_history})
# chat_history.append((question1, result["answer"]))
# print(result["answer"])
# print("-"*30)


# question2 = "What happens if the relevant docs exceed the 4k token limit?"
# result = qa({"question": question2, "chat_history": chat_history})
# print(result["answer"])
# print("-"*30)


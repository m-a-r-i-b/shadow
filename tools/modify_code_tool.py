import os

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS

from config import PROJ_ROOT_DIR
from prompt_templates.modify_code_prompt import get_formatted_prompt

class ModifyCodeTool():
    def __init__(self, llm) -> None:
        self._llm = llm
        self._db = self._loadDB()


    def _loadDB(self):
      embeddings = OpenAIEmbeddings(disallowed_special=())
      try :
          db = FAISS.load_local(PROJ_ROOT_DIR, embeddings)
          print("Found local DB")
      except:
          print("Local DB not found")

          docs = []
          for dirpath, dirnames, filenames in os.walk(PROJ_ROOT_DIR):
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
          db.save_local(PROJ_ROOT_DIR)
        
      return db


    # Vector search to return the file user is asking to modify
    # TODO : Maybe change to RetrivalChain? for better context understanding
    def _find_relevant_file(self, user_query: str):
      docs = self._db.similarity_search(user_query)
      
      if len(docs) == 0:
        return None, None
      
      return docs[0].metadata, docs[0].page_content


    def _execute_task(self, tasklet, _):
        # Find relevant file to make changes to
        filePath, fileContents = self._find_relevant_file(tasklet)
        
        print("Filepath = ",filePath)
        print("contents = ",fileContents)
        # Was unable to find relevant file or grab contents
        if (filePath or fileContents) is None:
          return "Was unable to perform given task, maybe try again with full context of the task"

        # Configure prompt template
        prompt = get_formatted_prompt(tasklet=tasklet,initial_code=fileContents)
        
        # Get raw result and return parsed output
        raw_result = self._llm(prompt)
        print("raw_result = ",raw_result)

        # Extract relevant output
        output = self._parse_output(raw_result)
        print("output = ",output)



        # Extract code from result and update to file

        return "code has been modified"
        # return self._parse_output(raw_result)


    def _parse_output(self, result):
        return result.content
    
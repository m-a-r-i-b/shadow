import os

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS

from config import PROJ_WORK_DIR
from prompt_templates.modify_code_template import get_formatted_prompt
from utils import is_acceptable_file_type

class ModifyCodeTool():
    def __init__(self, llm) -> None:
        self._llm = llm
        self._db = self._loadDB()


    def _loadDB(self):
        embeddings = OpenAIEmbeddings(disallowed_special=())
        # TODO : Re-load only the changed files, as opposed to re-calculating embeddings for every file everytime
        docs = []
        for dirpath, dirnames, filenames in os.walk(PROJ_WORK_DIR):
            print(dirnames)
            for file in filenames:
                if is_acceptable_file_type(file):
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
            db.save_local(PROJ_WORK_DIR)
        
        return db


    def execute_task(self, tasklet, _):
        # Find relevant file to make changes to
        file_path, file_contents = self._find_relevant_file(tasklet)
        
        print("file_path = ",file_path)
        print("contents = ",file_contents)
        # Was unable to find relevant file or grab contents
        if (file_path or file_contents) is None:
            print("Was unable to perform given task, maybe try again with full context of the task")

        # Configure prompt template
        prompt = get_formatted_prompt(tasklet=tasklet,initial_code=file_contents)
        
        # Get raw result and return parsed output
        raw_result = self._llm(prompt)
        print("raw_result = ",raw_result)

        # Extract relevant output
        new_file_contents = self._parse_output(raw_result)
        print("output = ",new_file_contents)

        self._write_to_file(file_path,new_file_contents)

    # Vector search to return the file user is asking to modify
    # TODO : Maybe change to RetrivalChain? for better context understanding
    def _find_relevant_file(self, user_query: str):
        docs = self._db.similarity_search(user_query)
      
        if len(docs) == 0:
            return None, None
      
        return docs[0].metadata['source'], docs[0].page_content


    def _parse_output(self, result):
        return result.content


    def _write_to_file(self, file_path: str, contents: str):
        with open(file_path, 'w') as file:
            file.write(contents)

    
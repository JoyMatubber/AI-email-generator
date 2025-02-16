# import pandas as pd
# import chromadb
# import uuid
#
#
# class Portfolio:
#     def __init__(self, file_path="app/resource/my_portfolio.csv"):
#         self.file_path = file_path
#         self.data = pd.read_csv(file_path)
#         self.chroma_client = chromadb.PersistentClient('vectorstore')
#         self.collection = self.chroma_client.get_or_create_collection(name="portfolio")
#
#     def load_portfolio(self):
#         if not self.collection.count():
#             for _, row in self.data.iterrows():
#                 self.collection.add(documents=row["Techstack"],
#                                     metadatas={"links": row["Links"]},
#                                     ids=[str(uuid.uuid4())])
#
#     def query_links(self, skills):
#         return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])

import pandas as pd
import chromadb
import uuid
import io


class Portfolio:
    def __init__(self, file_path=None, file_data=None):
        # print(file_data)
        if file_data is not None:
            self.data = pd.read_csv(io.StringIO(file_data.getvalue().decode("utf-8")))
            print('data',self.data)
        elif file_path is not None:
            self.data = pd.read_csv(file_path)
        else:
            raise ValueError("Either file_path or file_data must be provided.")
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(documents=row["Techstack"],
                                    metadatas={"links": row["Links"]},
                                    ids=[str(uuid.uuid4())])

    def query_links(self, skills):
        results = self.collection.query(query_texts=skills, n_results=2)
        return results['metadatas'] if results else []

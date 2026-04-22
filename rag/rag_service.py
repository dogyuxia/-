from langchain_core.documents import Document

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate


from model.factory import chat_model
from rag.vector_store import VectorStoreService
from utils.prompt_loader import load_rag_prompt


def print_prompt(prompt):
    print(prompt.to_string())
    return prompt
class RagSummarizeService:

    def __init__(self,vector_store:VectorStoreService):
        self.vector_store= vector_store
        self.retriver = self.vector_store.get_retriever()
        self.prompt_text = load_rag_prompt()
        self.prompt_template= PromptTemplate.from_template(self.prompt_text)
        self.model = chat_model
        self.chain = self._init_chain()



    def _init_chain(self):
        chain = self.prompt_template | print_prompt | self.model  | StrOutputParser()
        return chain

    def retriever_docs(self,query:str)->list[Document]:
        return self.retriver.invoke(query)

    def rag_summerize(self,query:str)-> str:
        context_docs= self.retriever_docs(query)
        context = ""
        counter = 0
        for doc in context_docs:
            counter+=1
            context += f"[参考资料]{counter}:{doc.page_content}|参考源数据{doc.metadata}\n"
        return self.chain.invoke(
            {
                "input" :query,
                "context":context,
            }
        )

if __name__ == '__main__':
    vs = VectorStoreService()

    # 再把它传入进去
    rag = RagSummarizeService(vector_store=vs)

    print(rag.rag_summerize("大户型适合什么扫地机器人"))
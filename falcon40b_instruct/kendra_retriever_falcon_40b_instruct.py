
from langchain.retrievers import AmazonKendraRetriever
from langchain.chains import RetrievalQA
from langchain import OpenAI
from langchain.prompts import PromptTemplate
from langchain import SagemakerEndpoint
from langchain.llms.sagemaker_endpoint import LLMContentHandler
import json
import os
import argparse



def build_chain():
    region = os.environ["AWS_REGION"]
    kendra_index_id = os.environ["KENDRA_INDEX_ID"]
    endpoint_name = os.environ["FALCON_40B_INSTRUCT_ENDPOINT"]

    class ContentHandler(LLMContentHandler):
        content_type = "application/json"
        accepts = "application/json"

        def transform_input(self, prompt: str, model_kwargs: dict) -> bytes:
            input_str = json.dumps({"inputs": prompt, "parameters": {**model_kwargs}})
            return input_str.encode('utf-8')
        
        def transform_output(self, output: bytes) -> str:
            response_json = json.loads(output.read().decode("utf-8"))
            return response_json[0]["generated_text"]

    content_handler = ContentHandler()

    llm=SagemakerEndpoint(
            endpoint_name=endpoint_name, 
            region_name=region, 
            model_kwargs={
                "temperature":1e-3, 
                # "min_length": 200,
                "max_length": 2048, 
                "max_new_tokens":200,
                # "num_return_sequences":1,
                # "top_k":1,
                "return_full_text": False
            },
            content_handler=content_handler
        )

    retriever = AmazonKendraRetriever(index_id=kendra_index_id)

    prompt_template = """
    The following is a friendly conversation between a human and an AI. 
    The AI is talkative and provides lots of specific details from its context.
    If the AI does not know the answer to a question, it truthfully says it 
    does not know.
    ```{context}```
    Instruction: Based on the above documents, provide a detailed answer for "{question}". 
    Solution:"""
    # prompt_template = """
    # Your task is to answer the question as truthfully as possible using the provided context, and if the answer is not contained within the text below, say "I don't know"
    
    # context: {context}

    # question: {question} 
    # """.strip()
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )
    chain_type_kwargs = {"prompt": PROMPT}
    qa = RetrievalQA.from_chain_type(
        llm, 
        chain_type="stuff", 
        retriever=retriever, 
        chain_type_kwargs=chain_type_kwargs,
        return_source_documents=True
    )
    return qa

def run_chain(chain, prompt: str, history=[]):
    result = chain(prompt)
    # To make it compatible with chat samples
    return {
        "answer": result['result'],
        "source_documents": result['source_documents']
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--question", help="for input question", default="What's SageMaker")
    args = parser.parse_args()

    chain = build_chain()
    result = run_chain(chain, args.question)
    print(result['answer'])
    if 'source_documents' in result:
        print('Sources:')
        for d in result['source_documents']:
          print(d.metadata['source'])
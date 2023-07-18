# Amazon Kendra RAG with Falcon 40B Instruct Foundation Model

**The example is based on github repo of AWS Blog - [Quickly build high-accuracy Generative AI applications on enterprise data using Amazon Kendra, LangChain, and large language models](https://aws.amazon.com/blogs/machine-learning/quickly-build-high-accuracy-generative-ai-applications-on-enterprise-data-using-amazon-kendra-langchain-and-large-language-models/)**

The purpose of the document is to provide guidance on demonstrating Amazon Kendra RAG integration with Falcon 40B Instruct foundation model from HuggingFace using Amazon SageMaker.

## Deployment Process

### Step 1. Amazon Kendra Stack Deployment

Please create a CloudFormation stack with [kendra-docs-index.yaml](./kendra-docs-index.yaml). Please note that the deployment may take approx. 45mins to provision Kendra index and loading default Amazon services (Amazon SageMaker, Amazon Kendra & Amazon Lex)

### Step 2. Deploy Falcon 40B Instruct Model

Please prepare a SageMaker Studio user and execute notebook [deploy-falcon-40b-instruct.ipynb](./deploy-falcon-40b-instruct.ipynb) to deploy the foundation model.

### Step 3. Create the virtual environment to test Kendra RAG with Falcon 40B Instruct model

* Create a virtual environment with Python 3.9

* Install the package

```
pip install -r requirement
```

* Run the test
```

export AWS_REGION="us-east-1"
export KENDRA_INDEX_ID="fa587068-4db8-4660-bd56-ea7397672c13"
export FALCON_40B_INSTRUCT_ENDPOINT="falcon-40b-instruct-12xl"

python kendra_retriever_falcon_40b_instruct.py
```




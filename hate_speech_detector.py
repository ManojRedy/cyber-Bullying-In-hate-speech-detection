import os
from huggingface_hub import InferenceClient

client = InferenceClient(
    provider="hf-inference",
    api_key=os.environ["<!--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-->"],
)

result = client.text_classification(
    "I like you. I love you",
    model="unitary/multilingual-toxic-xlm-roberta",
)
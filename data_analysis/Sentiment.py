from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
import numpy as np

MODEL = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
config = AutoConfig.from_pretrained(MODEL)
model = TFAutoModelForSequenceClassification.from_pretrained(MODEL)


def get_polarity(sentence):
    return [str(val) for val in list(model(tokenizer.encode(sentence, return_tensors='tf'))[0][0].numpy())]

def get_polarity_batch(batch,batch_max_size=32):
    input = [item for item in batch]
    polarities=list(get_polarity_batch_yield([entry[0] for entry in input],batch_max_size))
    dates = [entry[1] for entry in input]
    results = [(p,d) for d,p in zip(dates,polarities)]
    return iter(results)

def get_polarity_batch_yield(batch,batch_max_size=4):
    batch_size = len(batch)
    min=0
    max=batch_max_size
    while(min<batch_size):
        if max>=batch_size:
            max=batch_size-1
        for result in list(model(
            tokenizer.batch_encode_plus(
                batch[min:max],
                padding=True,
                truncation=True,
                return_attention_mask=True,
                max_length=64,
                return_tensors='tf'
            ))[0]):
            yield result.numpy().tolist()
        min+=batch_max_size
        max+=batch_max_size
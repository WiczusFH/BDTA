import redis
from pyspark import SparkContext
from data_analysis.Clean import clean
import json
from Clean import clean
# from Sentiment import get_polarity_batch
from data_access.Redis_Static_Loader import load_from_redis
from data_access.RedisAccess import RedisAccess
def expand_to_sentences_lambda(input_tuple):
    return [(x,input_tuple[1]) for x in str(input_tuple[0]).split(".") if len(x)>9]

def write(filename,data):
    with open(filename, 'w') as f:
        json.dump(data, f)


redis_host = 'localhost'
redis_port = 6379
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=1)


def sentiment_analysis(source):
    keys = redis_client.keys(f'{source}:*')
    sc = SparkContext()

    rdd = sc.parallelize(keys, numSlices=4)
    """Load data and assign date. """
    input_data = rdd.map(lambda x: (load_from_redis(x), str(x).split(":")[1]))
    """Clean"""
    data = input_data.map(lambda x: (clean(str(x[0])),x[1]))
    """Split to sentences [(sentence,date)]"""
    data = data.flatMap(lambda x: expand_to_sentences_lambda(x))
    """Assign Sentiment per Sentence"""
    ra2=RedisAccess(db=2)
    for dp in data.collect():
        ra2.persist_raw("nytsentences",dp[1],dp[0])


sentiment_analysis("nyt")


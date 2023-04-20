import redis
from pyspark import SparkContext
from data_analysis.Clean import clean
import json


def write(filename,data):
    with open(filename, 'w') as f:
        json.dump(data, f)


redis_host = 'localhost'
redis_port = 6379
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=0)


def count_entries(source):
    """
    Writes number of entries per day.
    Uses Spark RDD
    :param source:
    :return: None
    """
    keys = redis_client.keys(f'{source}:*')

    sc = SparkContext()
    rdd = sc.parallelize(keys, numSlices=4)

    input_data = rdd.map(lambda x: str(x).split(":")[1])
    data = input_data.map(lambda x: (x,1))
    entries_counts_per_day = data.reduceByKey(lambda x, y: x + y)
    entries_counts_per_day = entries_counts_per_day.map(lambda x: {'date':x[0],'count':x[1]})
    write(f"../flat_files/{source}_entry_counts.json", entries_counts_per_day.collect())


# count_entries("telegram")
count_entries("nyt")

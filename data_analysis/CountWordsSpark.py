import redis
from pyspark import SparkContext
from data_analysis.Clean import clean
from data_access.Redis_Static_Loader import load_from_redis
import json

redis_host = 'localhost'
redis_port = 6379
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=1)


def clean_with_replace_dot(text_date_tuple):
    return clean(str(text_date_tuple[0])).replace(".", " ")


def format_word(word:str):
    if len(word)==0:
        return word
    if len(word)==1:
        return word.upper()
    return word[0].upper()+word[1:].lower()


def expand_lambda_by_day(input_tuple):
    return [((format_word(x),input_tuple[1]),1) for x in str(input_tuple[0]).split(" ") if len(x)>0]


def expand_lambda_by_month(input_tuple):
    return [((format_word(x),input_tuple[1][0:6]),1) for x in str(input_tuple[0]).split(" ") if len(x)>0]


def expand_lambda_total(input_tuple):
    return [(format_word(x),1) for x in str(input_tuple[0]).split(" ") if len(x)>0]


def write(filename,data):
    with open(filename, 'w') as f:
        json.dump(data, f)


def count_words(source):
    """
    Counts words in a day, month, and total and saves the result into json.
    Uses Spark RDD.
    :param source:
    :return:
    """
    sc = SparkContext()
    keys = redis_client.keys(f'{source}:*')

    rdd = sc.parallelize(keys, numSlices=4)
    """Load data and assign date. """
    input_data = rdd.map(lambda x: (load_from_redis(x), str(x).split(":")[1]))
    """Clean"""
    data = input_data.map(lambda x: (clean_with_replace_dot(x), x[1]))
    """Split into words + dates. """
    data_by_day = data.flatMap(lambda x: expand_lambda_by_day(x))
    data_by_month = data.flatMap(lambda x: expand_lambda_by_month(x))
    data_total = data.flatMap(lambda x: expand_lambda_total(x))
    """Count"""
    output_by_day = data_by_day.reduceByKey(lambda x, y: x + y)
    output_by_month = data_by_month.reduceByKey(lambda x, y: x + y)
    output_total = data_total.reduceByKey(lambda x, y: x + y)
    """Save"""
    output_by_day = output_by_day.map(lambda x: {'word':x[0][0],'date':x[0][1], 'count':x[1]})
    output_by_month = output_by_month.map(lambda x: {'word':x[0][0],'date':x[0][1], 'count':x[1]})
    output_total = output_total.map(lambda x: {'word':x[0], 'count':x[1]})

    write(f"../flat_files/{source}_map_reduce_day.json",output_by_day.collect())
    write(f"../flat_files/{source}_map_reduce_month.json",output_by_month.collect())
    write(f"../flat_files/{source}_map_reduce_total.json",output_total.collect())


# count_words("telegram")
count_words("nyt")

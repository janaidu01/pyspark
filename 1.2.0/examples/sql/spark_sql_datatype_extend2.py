# coding: utf-8

"""Spark SQL DataType

ByteType: int
ShortType: int
IntegerType: int
LongType: long
FloatType: float
DoubleType: float
Decimal: Decimal
StringType: ""
BinaryType: ignore
BooleanType: bool
TimestampType: datetime
DateType: date
ArrayType: list
MapType: dict
StructType: tuple
"""

from pyspark import SparkConf, SparkContext
from pyspark.sql import HiveContext
import decimal
from datetime import datetime, date
from pyspark.sql import StructType, StructField, LongType

conf = SparkConf().setAppName("spark_sql_datatype_extend2")

sc = SparkContext(conf=conf)

hc = HiveContext(sc)

source = sc.parallelize(
    [(85070591730234615847396907784232501249, 85070591730234615847396907784232501249)])

schema = StructType([StructField("col1", LongType(), False),
                     StructField("col2", LongType(), False)])

table = hc.applySchema(source, schema)

table.registerAsTable("temp_table")

# java.lang.ClassCastException: java.math.BigInteger cannot be cast to
# java.lang.Long
rows = hc.sql(
    "select cast(col1 as decimal(38, 0)) + cast(col2 as decimal(38, 0)) from temp_table").collect()

sc.stop()

for row in rows:
    print row[0], isinstance(row[0], decimal.Decimal)

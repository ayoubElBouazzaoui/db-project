from pyspark.sql import SparkSession
import findspark
findspark.init("spark-3.3.1-bin-hadoop3")

# Or use this alternative
#findspark.init()")

# Or use this alternative
#findspark.init()


spark = SparkSession.builder \
   .master("local") \
   .appName("Linear Regression Model") \
   .config("spark.executor.memory", "1gb") \
   .getOrCreate()
   
sc = spark.sparkContext
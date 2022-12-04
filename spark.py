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

#create machine learning model using pyspark ml library 
from pyspark.ml.regression import LinearRegression
from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import VectorAssembler

#load data from database
df = spark.read.format("jdbc").options(

url="jdbc:postgresql://vichogent.be:40045/DEP",

driver="org.postgresql.Driver",

dbtable="dep.\"Onderneming\"",
user="postgres",
password="",
).load()

df.show()

df = df.select("ID","WebAdres","Naam")

assembler = VectorAssembler(inputCols=["ID","WebAdres","Naam"],outputCol="features")
output = assembler.transform(df)
final_data = output.select("features","Naam")

train_data,test_data = final_data.randomSplit([0.7,0.3])

lr = LinearRegression(labelCol='Naam')
lr_model = lr.fit(train_data)

test_results = lr_model.evaluate(test_data)
test_results.residuals.show()


unlabeled_data = test_data.select('features')
predictions = lr_model.transform(unlabeled_data)
predictions.show()

lr_model.save("lr_model")

from pyspark.ml.regression import LinearRegressionModel
lr_model = LinearRegressionModel.load("lr_model")


unlabeled_data = test_data.select('features')
predictions = lr_model.transform(unlabeled_data)
predictions.show()


















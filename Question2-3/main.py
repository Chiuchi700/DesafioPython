from pyspark.sql import SparkSession
from pyspark.sql.functions import *


def question2(spark):
    transacao = [{"transacao_id": 1, "total_bruto": 3000, "desconto_percentual": 6.99},
                 {"transacao_id": 2, "total_bruto": 57989, "desconto_percentual": 1.45},
                 {"transacao_id": 4, "total_bruto": 1, "desconto_percentual": None},
                 {"transacao_id": 5, "total_bruto": 34, "desconto_percentual": 0.0}]

    # criando o dataframe e preenchendo os campos que estão vazios com 0
    df_transaco = spark.createDataFrame(transacao).fillna(0)

    # criando uma nova coluna que está aplicando a porcentagem de desconto no valor bruto
    df_calculo_desconto = df_transaco \
        .withColumn("total_descontado", col("total_bruto") - (col("total_bruto") * (col("desconto_percentual") / 100)))

    # selecionando a coluna calculada acima para somar seus valores e colocar com 2 casas decimais
    df_totl_liquido = df_calculo_desconto\
        .select(format_number(sum(col("total_descontado")), 2).alias("total_liquido"))

    df_totl_liquido.show()


def question3(spark):

    # carregando o arquivos de dados json e como está em uma lista, o parâmetro multiline foi incluído
    df_json_data = spark.read.option("multiline", "true").json("data.json")

    # utilizando o método explode para remover a lista de valores da coluna ItemList
    df_exploded = df_json_data.withColumn("Items", explode("ItemList")).drop("ItemList")

    # acessando as colunas que estão aninhadas e removendo da lista de valores para que elas possam ser independentes
    df_exploded_columns = df_exploded.withColumn("ProductName", col("Items.ProductName"))\
        .withColumn("Quantity", col("Items.Quantity"))\
        .withColumn("Value", col("Items.Value"))\
        .drop("Items")

    # transformando em modelo relacional, logo, removendo a coluna de lista do dataframe
    df_transactions = df_json_data.drop("ItemList")

    # formando o dataframe de produtos, onde estaroa ligado com o df_transactions pela coluna "NFeID"
    df_products = df_exploded_columns.select("NFeID", "ProductName", "Quantity", "Value")

    df_transactions.show(truncate=False)
    df_products.show()


def main():

    # criação da SparkSession
    spark = SparkSession\
        .builder\
        .appName("Lambda3")\
        .master("local[*]")\
        .getOrCreate()

    print("Questão 2: \n")
    question2(spark)

    print("Questão 3: \n")
    question3(spark)


if __name__ == "__main__":
    main()

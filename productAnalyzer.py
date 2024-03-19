# Arquivo: product_analyzer.py

from database import Database
from helper.writeAJson import writeAJson

class ProductAnalyzer:
    def __init__(self, database, collection):
        self.db = Database(database=database, collection=collection)

    def total_vendas_por_dia(self):
        pipeline = [
            {"$unwind": "$produtos"},
            {"$group": {
                "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$data_compra"}},
                "total_vendido": {"$sum": {"$multiply": ["$produtos.quantidade", "$produtos.preco"]}}
            }},
            {"$project": {
                "_id": 0,  # Remove o campo _id
                "data_compra": "$_id",  # Renomeia _id para data_compra
                "total_vendido": 1  # Mantém o campo total_vendido
            }}
        ]
        result = self.db.collection.aggregate(pipeline)
        writeAJson(result, "Total de vendas por dia")


    def produto_mais_vendido(self):
        pipeline = [
            {"$unwind": "$produtos"},
            {"$group": {"_id": "$produtos.descricao", "total_vendido": {"$sum": "$produtos.quantidade"}}},
            {"$sort": {"total_vendido": -1}},
            {"$limit": 1}
        ]
        result = self.db.collection.aggregate(pipeline)
        writeAJson(result, "Produto mais vendido")

    def cliente_mais_gastou_em_uma_unica_compra(self):
        pipeline = [
            {"$unwind": "$produtos"},
            {"$group": {"_id": {"cliente": "$cliente_id", "compra": "$_id"}, 
                        "total_gasto": {"$sum": {"$multiply": ["$produtos.quantidade", "$produtos.preco"]}}}},
            {"$sort": {"total_gasto": -1}},
            {"$group": {"_id": "$_id.cliente", "maior_gasto": {"$first": "$total_gasto"}}},
            {"$sort": {"maior_gasto": -1}},
            {"$limit": 1},
            {"$project": {"_id": 0, "cliente_maior_gasto": "$_id", "total_gasto": "$maior_gasto"}}
        ]


        result = self.db.collection.aggregate(pipeline)
        writeAJson(result, "Cliente que mais gastou em uma única compra")

    def produtos_com_quantidade_acima_de_um(self):
        pipeline = [
            {"$unwind": "$produtos"},
            {"$group": {"_id": "$produtos.descricao", "total_vendido": {"$sum": "$produtos.quantidade"}}},
            {"$match": {"total_vendido": {"$gt": 1}}}
        ]
        result = self.db.collection.aggregate(pipeline)
        writeAJson(result, "Produtos com quantidade vendida acima de 1 unidade")

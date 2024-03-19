from database import Database
from writeAJson import writeAJson
import json

class ProductAnalyzer:
    def __init__(self, db: Database):
        self.db = db

    def maximodevendasdia(self):
        resultado = list(self.db.collection.aggregate([
            {"$group": {"_id": "$data_compra", "total_vendido": {"$sum": 1}}}
        ]))
        writeAJson(resultado, "Total vendas no dia")
        return resultado

    def maisvendido(self):
        resultado = list(self.db.collection.aggregate([
            {"$unwind": "$produtos"},
            {"$group": {"_id": "$produtos.descricao", "total_vendido": {"$sum": "$produtos.quantidade"}}},
            {"$sort": {"total_vendido": -1}},
            {"$limit": 1}
        ]))
        writeAJson(resultado, "Produto mais vendido")
        return resultado

    def maiorgasto(self):
        resultado = list(self.db.collection.aggregate([
            {"$unwind": "$produtos"},
            {"$group": {"_id": "$cliente_id",
                        "total_vendido": {"$sum": {"$multiply": ["$produtos.quantidade", "$produtos.preco"]}}}},
            {"$sort": {"total_vendido": -1}},
            {"$limit": 1}
        ]))
        writeAJson(resultado, "Maior gasto por cliente")
        return resultado

    def produtoscomvendas(self):
        resultado = list(self.db.collection.aggregate([
            {"$unwind": "$produtos"},
            {"$match": {"produtos.quantidade": {"$gt": 1}}},
            {"$group": {"_id": "$produtos.descricao"}}
        ]))
        writeAJson(resultado, "Produtos com mais de uma venda")
        return resultado

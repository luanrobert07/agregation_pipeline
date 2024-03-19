from database import Database
from helper.writeAJson import writeAJson
from productAnalyzer import ProductAnalyzer

# Inicializar a conexão com o banco de dados
db = Database(database="mercado", collection="compras")
db.resetDatabase()

    # Inicializar a instância de ProductAnalyzer
analyzer = ProductAnalyzer(database="mercado", collection="compras")

    # Executar as análises usando os métodos de ProductAnalyzer
analyzer.produto_mais_vendido()
analyzer.cliente_mais_gastou_em_uma_unica_compra()
analyzer.produtos_com_quantidade_acima_de_um()
analyzer.total_vendas_por_dia()

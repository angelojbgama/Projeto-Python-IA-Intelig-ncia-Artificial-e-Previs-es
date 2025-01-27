import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

# Carregar a base de dados
# O arquivo "clientes.csv" contém os dados dos clientes, incluindo características e o score de crédito.
tabela = pd.read_csv("clientes.csv")
print(tabela.head())  # Exibe as primeiras linhas da tabela para inspecionar os dados

# Verificar dados faltantes ou com formato errado
# Aqui verificamos o tipo de dados de cada coluna e se existem valores nulos.
print(tabela.info())

# Codificar colunas de texto em números
# O LabelEncoder transforma valores categóricos (strings) em valores numéricos para que possam ser utilizados pelos modelos.
codificador = LabelEncoder()
for coluna in tabela.columns:
    # Apenas colunas de texto e que não sejam a coluna-alvo ("score_credito") são transformadas.
    if tabela[coluna].dtype == "object" and coluna != "score_credito":
        tabela[coluna] = codificador.fit_transform(tabela[coluna])

# Verificar novamente os tipos das colunas para garantir que a codificação foi aplicada corretamente.
print(tabela.info())

# Separar as features (X) e o alvo (y)
# X contém todas as colunas usadas como entrada para o modelo, exceto "score_credito" e "id_cliente" (irrelevante para o modelo).
# y é a coluna que queremos prever: o score de crédito.
x = tabela.drop(["score_credito", "id_cliente"], axis=1)
y = tabela["score_credito"]

# Dividir os dados em treino e teste
# 70% dos dados serão usados para treinar o modelo, e 30% serão usados para testá-lo.
x_treino, x_teste, y_treino, y_teste = train_test_split(x, y, test_size=0.3, random_state=1)

# Criar os modelos
# RandomForestClassifier: Modelo baseado em árvores de decisão.
# KNeighborsClassifier: Modelo baseado no algoritmo dos k-vizinhos mais próximos.
modelo_arvore = RandomForestClassifier()
modelo_knn = KNeighborsClassifier()

# Treinar os modelos
# Ambos os modelos aprendem a relação entre as features (x_treino) e os scores de crédito (y_treino).
modelo_arvore.fit(x_treino, y_treino)
modelo_knn.fit(x_treino, y_treino)

# Fazer previsões com os dados de teste
# Aqui geramos previsões com os dois modelos treinados para comparar com os valores reais.
previsao_arvore = modelo_arvore.predict(x_teste)
previsao_knn = modelo_knn.predict(x_teste.to_numpy())

# Calcular a acurácia dos modelos
# Compara as previsões feitas pelos modelos com os valores reais (y_teste).
acuracia_arvore = accuracy_score(y_teste, previsao_arvore)
acuracia_knn = accuracy_score(y_teste, previsao_knn)

# Exibir a acurácia de ambos os modelos
print(f"Acurácia - Random Forest: {acuracia_arvore}")
print(f"Acurácia - KNN: {acuracia_knn}")

# Visualizar a distribuição dos scores de crédito na base de dados
# Cria um gráfico de barras com a contagem de cada categoria de score de crédito.
contagem_scores = tabela["score_credito"].value_counts()
contagem_scores.plot(kind='bar', title='Distribuição dos Scores de Crédito')
plt.xlabel('Score de Crédito')
plt.ylabel('Quantidade')
plt.show()

# Comparar a acurácia dos modelos usando um gráfico de barras
plt.bar(["Random Forest", "KNN"], [acuracia_arvore, acuracia_knn], color=['blue', 'green'])
plt.title('Acurácia dos Modelos')
plt.ylabel('Acurácia')
plt.show()

# Identificar a importância das características (features)
# O modelo Random Forest calcula automaticamente a importância de cada feature no processo de decisão.
importancia = pd.DataFrame(index=x.columns, data=modelo_arvore.feature_importances_ * 100, columns=['Importância'])
importancia.sort_values(by='Importância', ascending=False, inplace=True)

# Visualizar a importância das features em um gráfico de barras
importancia.plot(kind='bar', title='Importância das Características', legend=False)
plt.ylabel('Importância (%)')
plt.show()

# Prever o score de crédito para novos clientes
# Carregar o arquivo "novos_clientes.csv" com dados dos clientes para os quais queremos prever o score.
novos_clientes = pd.read_csv("novos_clientes.csv")
print(novos_clientes.head())  # Exibe as primeiras linhas do arquivo

# Codificar colunas de texto no conjunto de novos clientes
for coluna in novos_clientes.columns:
    if novos_clientes[coluna].dtype == "object":
        novos_clientes[coluna] = codificador.fit_transform(novos_clientes[coluna])

# Fazer previsões com o modelo Random Forest
previsoes = modelo_arvore.predict(novos_clientes)
print("Previsões para novos clientes:", previsoes)

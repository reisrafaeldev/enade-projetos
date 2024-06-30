import pdfplumber
import re
import pandas as pd

def extrair_questoes(texto):
    padrao_questao = re.compile(r'(QUESTÃO \d+|QUESTÃO DISCURSIVA \d+)', re.IGNORECASE)
    questoes = padrao_questao.split(texto)

    questoes = questoes[1:]

    questoes_formatadas = []
    for i in range(0, len(questoes), 2):
        numero = questoes[i].strip()
        if i + 1 < len(questoes):
            texto_questao = questoes[i + 1].strip()
            questoes_formatadas.append((numero, texto_questao))

    return questoes_formatadas

questoes_array = []

with pdfplumber.open('../BSI/2021/2021_PV_bacharelado_sistema_informacao.pdf') as pdf:
    for pagina in pdf.pages:
        texto = pagina.extract_text()
        if texto:
            questoes = extrair_questoes(texto)
            questoes_array.extend(questoes)

dados = {
    "numero_questao": [q[0] for q in questoes_array],
    "texto_questao": [q[1] for q in questoes_array],
    "classificacao": ["bsi"] * len(questoes_array),
    "prova_contida": ["Sistemas de Informação"] * len(questoes_array),
    "ano_questao": [2021] * len(questoes_array),
    "opcao_correta": [None] * len(questoes_array)
}

df = pd.DataFrame(dados)

df.to_csv('../questoes_extracao.csv', index=False)

print("As questões foram extraídas e salvas no arquivo 'questoes_extracao.csv'.")

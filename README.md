# Sistema de Comparação de Imagens

Este repositório apresenta uma aplicação para análise de similaridade entre duas imagens utilizando técnicas de visão computacional. O sistema identifica pontos de interesse, compara descritores e valida correspondências para determinar se as imagens podem representar o mesmo local ou estrutura, mesmo sob variações de ângulo ou iluminação.

## 📌 Visão Geral

A aplicação fornece uma interface gráfica simples, permitindo selecionar duas imagens e visualizar o resultado da comparação. As correspondências válidas são destacadas visualmente e também exportadas para arquivos na pasta de resultados.

## 🛠 Funcionalidades

- Interface construída em Tkinter.
- Detecção de keypoints com ORB.
- Comparação de descritores via BFMatcher.
- Filtragem de correspondências com:
  - Ratio Test
  - Homografia estimada por RANSAC
- Geração de imagens de saída contendo:
  - Correspondências válidas
  - Pontos de interesse relevantes
- Salvamento automático dos resultados.

## 📁 Estrutura do Projeto

```
/projeto
 ├── main.py
 ├── resultados/
 ├── requirements.txt
 └── README.md
```

## 🔧 Dependências

Requer Python 3.x e as bibliotecas:

- opencv-python
- numpy
- pillow

Instalação recomendada:

```
pip install -r requirements.txt
```

## ▶️ Como Executar

### 1. Clone o repositório

```
git clone <seu-repositorio>
cd <pasta-do-projeto>
```

### 2. Crie e ative um ambiente virtual

**Windows (PowerShell):**
```
python -m venv venv
./venv/Scripts/Activate.ps1
```

**Linux/macOS:**
```
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```
pip install -r requirements.txt
```

### 4. Execute a aplicação

```
python main.py
```

Selecione as duas imagens e inicie a comparação.

## 📁 Resultados Gerados

A aplicação salva automaticamente as seguintes imagens na pasta `resultados/`:

- Comparação com linhas entre correspondências válidas
- Comparação destacando keypoints relevantes
- Painel com todos os pontos-chave válidos

## 🧠 Funcionamento Interno

Fluxo de processamento:

1. Carregamento das imagens (cinza + cor).
2. Detecção de pontos de interesse via ORB.
3. Extração e comparação dos descritores.
4. Ratio Test para filtrar correspondências ambíguas.
5. RANSAC para validar a geometria da transformação entre imagens.
6. Construção da imagem final com correspondências confiáveis.

## 📴 Encerrar o ambiente virtual

```
deactivate
```

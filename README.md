<a href="https://github.com/Clube-dos-5">
    <img src="https://github.com/Clube-dos-5/Toledo/blob/Dev-FaKL/CD5LogoDark.png" alt="CD5 logo" title="CD5" align="right" height="60" />
</a>

# Toledo - Visão Computacional com Python

[![Github All Releases](https://img.shields.io/github/downloads/Clube-dos-5/Toledo/total.svg)]()
<img src="https://komarev.com/ghpvc/?username=Clube-dos-5&color=brightgreen" alt="watching_count" />
[![python](https://img.shields.io/badge/Python-3.9-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)


<a href="https://www.fiap.com.br">
    <img src="https://github.com/Clube-dos-5/Toledo/blob/Dev-FaKL/fiap.png" alt="FIAP logo" title="FIAP" align="right" height="60" />
</a>

## Challenge Sprint 2023

Para a atividade do Challenge Sprint 2023, foi apresentado um desafio que consiste em prevenir fraudes na pesagem de caminhões, utilizando conceitos e praticas ensinados no curso de Engenharia da Computação.

### Desafio

Identificar possíveis anomalias ou tentativas de fraude durante a pesagem de caminhões.

### Sistema Atual

Hoje, o sistema de pesagem possui diversos mecanismos antifraude como cartões RFID que são distibuídos às pessoas para identificação

### Possíveis Melhorias
- Detectar a presença de pessoas ou outros objetos sobre a balaça no momento da pesagem(Visão Computacional).
- Funcionamento anormal das células de carga (Ciência de Dados).
- Variação anormal do peso dos veículos (Ciência de Dados).

## Escopo do Projeto

Nosso escopo consiste somente nas pesagens que acontecem com caminhões para transporte (meio do caminho e final) de cargas, não abrangendo pesagem de produtos em lojas, fábricas, nem mecanismos de cancelas automáticas ou manuseadas por funcionários.

## Especificação do Projeto

A proposta deste projeto é desenvolver um sistema que utilize visão computacional e a biblioteca [YOLO](https://opencv-tutorial.readthedocs.io/en/latest/yolo/yolo.html#), a qual já possui uma base de dados, para identificar se o caminhão está mal posicionado na balança. Por meio dessa abordagem, poderemos detectar e verificar o posicionamento dos caminhões estacionados na balança, reduzindo significativamente as possibilidades de fraude.

# Componentes do Grupo:

## 4ECR
Carlos Borges - RM84613 \
[![Carlos github](https://img.shields.io/badge/GitHub-kmuv1t-181717.svg?style=flat&logo=github)](https://github.com/kmuv1t) \
Erik Evaristo - RM81052 \
[![Erik github](https://img.shields.io/badge/GitHub-ErikFRC-181717.svg?style=flat&logo=github)](https://github.com/ErikFRC) \
Eduardo Stefano - RM84498 \
[![Eduardo github](https://img.shields.io/badge/GitHub-dugimenes--jpg-181717.svg?style=flat&logo=github)](https://github.com/dugimenes-jpg) 
## 4ECA
Fábio Pipek - RM84566 \
[![Fábio github](https://img.shields.io/badge/GitHub-fabiopipek-181717.svg?style=flat&logo=github)](https://github.com/fabiopipek) \
Guilherme Cabrini - RM84189 \
[![Guilherme github](https://img.shields.io/badge/GitHub-cabrinii-181717.svg?style=flat&logo=github)](https://github.com/cabrinii) \
Marcos Cantelli - RM84582 \
[![Marcos github](https://img.shields.io/badge/GitHub-MrHighTech20-181717.svg?style=flat&logo=github)](https://github.com/MrHighTech20) 


# Sumário

- [Instalação](#instalação)
    - [Setup](#setup)
- [Iniciar](#iniciar)
- [Testes](#testes)
- [Links](#links)

# Instalação

## Requisitos

- [Python 3.9](https://www.python.org/downloads/)
- [Pip](https://pip.pypa.io/en/stable/installing/)
- [Git](https://git-scm.com/downloads) - (opcional, mas recomendado para clonar o projeto e atualizar as versões)

## Setup
1. Faça o download da última versão ou clone o projeto na sua máquina local usando:
```bash
git clone https://github.com/Clube-dos-5/Toledo.git
```

2. Crie um ambiente virtual:

- No Windows usando:

```bash
python -m venv venv
``` 
- No Linux usando:

```bash
virtualenv --python python3 venv
```
3. Ative o ambiente virtual:

- No Windows usando:

```bash
venv\Scripts\activate.bat
```
- No Linux usando:

```bash
source venv/bin/activate
```

4. Instale as dependências usando:
```bash
pip install -r requirements.txt
```

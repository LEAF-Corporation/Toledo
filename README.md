<h1 style="text-align: center;">
    <img src="src/mosq.png" alt="Mosqueteiros Logo" title="Mosqueteiros" height="120" />
    <br>
    FIAP Challenge -  2023
</h1>
<p style="text-align: center;">Toledo do Brasil - Indústria de Balanças Ltda.</p>
<h2 style="text-align: center;">Visão Computacional com Python</h2>


[![python](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=yellow)](https://www.python.org)
[![opencv](https://img.shields.io/badge/lib-OpenCV-green)](https://www.opencv.org)
[![pytorch](https://img.shields.io/badge/lib-PyTorch-orange)](https://pytorch.org)

Para o Challenge 2023, decidimos desenvolver uma solução para mitigar vulnerabilidades existentes na etapa pesagem de caminhões utilizando visão computacional. Com esta solução poderemos evitar eventuais fraudes e adulterações no processo.

### Desafio

Evitar e mitigar qualquer possível adulteração ou tentativa de fraude durante o processo de pesagem.

### Sistema Atual

Hoje, o sistema de pesagem possui alguns mecanismos antifraude como cartões RFID que são distribuídos para fins de identificação

### Possíveis Melhorias
- Detectar e alertar a presença de pessoas no perímetro do local de pesagem (Visão Computacional).
- Alertar posicionamento incorreto do caminhão na balança (Visão Computacional).

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

- [Python 3.11](https://www.python.org/downloads/)
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

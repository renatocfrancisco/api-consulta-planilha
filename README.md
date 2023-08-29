# api-consulta-maciça

![Python](https://img.shields.io/badge/python-3670A0?style=flat&logo=python&logoColor=ffdd54)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=flat&logo=pandas&logoColor=white)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=flat&logo=flask&logoColor=white)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

API Flask com requisição POST para retornar um `.csv`, filtrando e consultando planilhas.

## Requisitos e comandos

- Precisa-se da pasta de planilhas (no código, pasta: `csv`), arquivos csv divididos em estados (ex: `SP.csv`)
- `py -m venv venv`, `.\venv\Scripts\activate` e `deactivate` para usar ambiente de desenvolvimento python
- `pip install -r requirements.txt` para instalar dependências
- `flask --app main run` para executar main.py com Flask

## Colunas para filtrar

- Idade - `idade`
- Valor de parcela - `parcela`
- Quantidade de parcela paga - `soma parcela`
- Espécie Benefício - `esp`
- Banco de Empréstimo - `banco emp`
- Banco de Pagamento - `banco PGTO`
- Taxa de juros - `juros`

### Colunas das planilhas do projeto

```csv
cpf;nome;dt-nasc;esp;banco emp;nb;ctt;prazo;parcela;emprestado;inicio;fim;averbacao;ID_ORIGEM;cpf;cidade;uf;vl beneficio;dib;banco PGTO;meio_pgto;bairro;endereco;cep;agencia PGTO;FONE1;FONE2;FONE3;cpf;soma parcela;vl beneficio;margem;juros;idade
```

## Body da requisição (json)

Exemplo:

```json
{
  "uf": ["SP","TO"],
  "idadeMin": 80,
  "idadeMax": 80,
  "parcelaMin": 50,
  "parcelaMax": 400,
  "parcelasPagasMin": 70,
  "parcelasPagasMax": 500,
  "jurosMin": 1,
  "jurosMax": 2,
  "esp": [21, 41],
  "banco_emp": [1, 2],
  "banco_pgto": [104,237]
}
```

Utilizar `["ALL"]` em "esp", "banco_emp", "banco_pgto" para filtrar todos os valores de espécie e banco.

<details>
  <summary>Developer Commentary</summary>

  Aprendi um pouco de Flask e ainda melhorei o código de consulta de planilhas que precisavam.
  Pandas pra sempre :)
  
</details>

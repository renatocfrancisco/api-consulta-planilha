# script-consulta-maciça

Usando um json como filtro, `main.py` retorna um csv com os dados filtrados.
Precisa-se da pasta de planilhas e do arquivo `data.json` para testar.

## Colunas para filtrar

- Idade - `idade`
- Valor de parcela - `parcela`
- Qnt parcela paga - `soma parcela`
- Espécie Benefício - `esp`
- UF - `?`
- Banco Empréstimo - `banco emp`
- Banco de Pagamento - `banco PGTO`
- Taxa juros - `juros`

## data.json

Exemplo:

```json
{
  "idade": {
    "min": 80,
    "max": 80
  },
  "parcela": {
    "min": 50,
    "max": 400
  },
  "soma_parcela": {
    "min": 70,
    "max": 500
  },
  "esp": [21, 41],
  "banco_emp": [1, 2],
  "banco_pgto": [104,237]
}

```

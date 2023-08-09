# script-consulta-maciça

Usando um json como filtro, `filter.py` retorna um csv com os dados filtrados.

Precisa-se da pasta de planilhas e do arquivo `data.json` para testar.

## Colunas para filtrar

- Idade - `idade`
- Valor de parcela - `parcela`
- Quantidade de parcela paga - `soma parcela`
- Espécie Benefício - `esp`
- Banco de Empréstimo - `banco emp`
- Banco de Pagamento - `banco PGTO`
- Taxa de juros - `juros`

## data.json

Exemplo:

```json
{
  "uf": ["SP","TO"],
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
  "juros":{
    "min": 1,
    "max": 2
  },
  "esp": [21, 41],
  "banco_emp": [1, 2],
  "banco_pgto": [104,237]
}
```

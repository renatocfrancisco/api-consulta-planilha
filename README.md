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

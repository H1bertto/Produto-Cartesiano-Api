# Produto Cartesiano - Api

### Exemplos de Post

- Operação:

```json
{
  "conjunto_a": [1, 2, 3],
  "conjunto_b": [1, 4, 5],
  "operacao": "+",
  "logica": {}
}
```

- Lógica:

```json
{
  "conjunto_a": [1, 2, 3],
  "conjunto_b": [1, 4, 5],
  "operacao": "",
  "logica": {"a": "primo", "b": "impar"}
}
```


#

### Exemplo de Resposta

- Resposta:

```json
{
  "resposta": [[1, 1], [1, 2], [1, 3]],
  "modulo": 3
}
```
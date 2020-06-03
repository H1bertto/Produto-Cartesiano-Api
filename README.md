# Produto Cartesiano - Api

### Endpoints


 - ``/`` - Home da API

 - ``/calculate/`` - Realiza as operações e lógicas entre conjutos


### Exemplos de Post

- Operação:

```json
{
  "conjunto_a": [1, 2, 3],
  "conjunto_b": [2, 4],
  "operacao": "+",
  "logica": {}
}
```

- Lógica:

```json
{
  "conjunto_a": [1, 2, 3],
  "conjunto_b": [2, 4],
  "operacao": "",
  "logica": {"a": "primo", "b": "impar"} ou "a+b=<numero>"
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
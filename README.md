# Trabalho de Matemática Discreta

**Tema:** Produto Cartesiano

### API - Docs:
#### Endpoints


 - ``/`` - Home da API

 - ``/calculate/`` - Realiza as operações e lógicas entre conjutos


#### Exemplos de Post

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

```bash
{
  "conjunto_a": [1, 2, 3],
  "conjunto_b": [2, 4],
  "operacao": "",
  "logica": {"a": "primo", "b": "impar"} ou "a+b=<numero>"
}
```


#

#### Exemplo de Resposta

- Resposta:

```json
{
  "conjunto_universo": [[1, 2], [1, 4], [2, 2], [2, 4], [3, 2], [3, 4]],
  "modulo_conjunto_universo": 6,
  "resposta": [[2, 2]],
  "modulo_resposta": 1
}
```
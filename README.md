# url-checker v2

Script desenvolvido em **Python** para verificar o status HTTP de uma lista de URLs.

O programa lê as URLs do arquivo `base/2024/rj.txt`, realiza uma requisição HTTP para cada endereço e separa as URLs de acordo com o resultado:

- `200` — URL acessível
- `404` — Página não encontrada
- Outros códigos — exibidos no terminal
- Erros de requisição — exibidos no terminal

Os resultados dos códigos `200` e `404` são armazenados em arquivos separados.

## Tecnologias utilizadas

- **Python 3**
- **Requests** — realização das requisições HTTP
- **Colorama** — exibição de mensagens coloridas no terminal

 ## Instalação

Certifique-se de ter o Python instalado.

Instale as dependências com:

```
pip install requests colorama
```

Ou, caso esteja utilizando `pip3`:

```
pip3 install requests colorama
```

## Estrutura do projeto

O programa espera encontrar os arquivos e diretórios seguindo esta estrutura:

```
.
├── base/
│   └── 2024/
│       └── rj.txt
│
├── resultado/
│   ├── 200.csv
│   └── 404.csv
│
└── main.py
```

## Arquivo de entrada

As URLs devem ser adicionadas ao arquivo:

```
base/2024/rj.txt
```

Cada URL deve estar em uma linha diferente:

```
https://www.google.com
https://www.python.org
https://www.exemplo.com/pagina
```

Linhas vazias são ignoradas automaticamente pelo programa.

## Execução

Execute o arquivo Python:

```
python main.py
```

Durante a execução, o programa apresenta cada URL e o status HTTP retornado.

Exemplo:

```
https://www.google.com
STATUS CODE 200

https://www.exemplo.com/pagina-inexistente
STATUS CODE 404

https://www.site.com
STATUS CODE 301
```

As mensagens são exibidas com cores diferentes no terminal:

- 🟢 Verde para `200`
- 🔴 Vermelho para `404`
- 🟡 Amarelo para outros códigos HTTP

## Resultados

As URLs que retornarem `HTTP 200` são salvas em:

```
resultado/200.csv
```

As URLs que retornarem `HTTP 404` são salvas em:

```
resultado/404.csv
```

Ao final da execução, o programa apresenta um resumo:

```
--------------------------------------------------
Resultado
--------------------------------------------------
10 URLs tiveram Status Code 200 OK
5 URLs tiveram Status Code 404 Page Not Found
--------------------------------------------------
```

## Tratamento de erros

O programa utiliza `requests.RequestException` para tratar erros durante as requisições.

Caso uma URL não possa ser acessada, o erro será exibido no terminal e o programa continuará processando as demais URLs.

Exemplo:

```
Erro ao acessar https://exemplo.com: ...
```

## Como o código funciona

O fluxo principal do programa é:

```
Arquivo rj.txt
      │
      ▼
Lê uma URL
      │
      ▼
Realiza requisição HTTP
      │
      ├── 200 ──► resultado/200.csv
      │
      ├── 404 ──► resultado/404.csv
      │
      └── Outros ──► Exibe no terminal
```

O programa também utiliza `with` para abrir os arquivos, garantindo que eles sejam fechados corretamente após o processamento.

## Dependências

As dependências utilizadas são:

```
requests
colorama
```

Elas podem ser instaladas com:

```
pip install requests colorama
```

## Observações

O código atualmente não utiliza `timeout` nas requisições HTTP. Portanto, dependendo do comportamento de um servidor, uma requisição pode permanecer aguardando por um período prolongado.

Além disso, somente os códigos `200` e `404` são gravados nos arquivos de resultado. Outros códigos HTTP são apenas exibidos no terminal.

## Licença

Este projeto não possui uma licença especificada. Caso seja publicado no GitHub ou distribuído publicamente, recomenda-se definir uma licença apropriada.


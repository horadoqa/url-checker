# url-checker

 Script em Python para verificar o **status HTTP de uma lista de URLs**, separando os resultados em arquivos CSV de acordo com o código retornado pelo servidor.

 Atualmente, o projeto identifica principalmente:

- 🟢 `200` — URL acessível / OK
- 🔴 `404` — Página não encontrada
- 🟡 Outros códigos HTTP — exibidos no terminal, mas não armazenados nos arquivos de resultado

## 📋 Requisitos

- Python 3.8 ou superior
- `requests`
- `colorama`

 ## 🚀 Instalação

Clone o projeto:

```
git clone git@github.com:horadoqa/url-checker.git
cd url-checker
```

Crie um ambiente virtual:

```
python -m venv venv
```

Ative o ambiente virtual.

### Linux / macOS

```
source venv/bin/activate
```

### Windows

```
venv\Scripts\activate
```

Instale as dependências:

```
pip install requests colorama
```

## 📁 Estrutura do projeto

A estrutura esperada é:

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
├── main.py
└── README.md
```

### Arquivo `rj.txt`

O arquivo `base/2024/rj.txt` deve conter **uma URL por linha**:

```
https://exemplo.com
https://google.com
https://site-inexistente.com
```

 Linhas vazias são ignoradas automaticamente.

 ## ▶️ Executando

 Com as dependências instaladas, execute:

```
python main.py
```

 Durante a execução, o programa exibe cada URL e seu respectivo status HTTP:

```
https://exemplo.com
STATUS CODE 200

https://site-inexistente.com
STATUS CODE 404

https://outro-site.com
STATUS CODE 301
```

Ao final, é apresentado um resumo:

```
--------------------------------------------------
Resultado
--------------------------------------------------
10 URLs tiveram Status Code 200 OK
3 URLs tiveram Status Code 404 Page Not Found
--------------------------------------------------
```

## 📊 Resultados

As URLs com status `200` são salvas em:

```
resultado/200.csv
```

As URLs com status `404` são salvas em:

```
resultado/404.csv
```

Por exemplo:

### `resultado/200.csv`

```
https://google.com
https://example.com
```

### `resultado/404.csv`

```
https://site-inexistente.com
https://example.com/pagina-inexistente
```

 ## 🧠 Como funciona

 O programa:

1. Abre o arquivo `base/2024/rj.txt`.
2. Percorre cada URL encontrada.
3. Ignora linhas vazias.
4. Realiza uma requisição HTTP utilizando a biblioteca `requests`.
5. Verifica o código de status retornado.
6. Salva URLs com status `200` em `resultado/200.csv`.
7. Salva URLs com status `404` em `resultado/404.csv`.
8. Exibe outros códigos HTTP no terminal.
9. Trata erros de conexão através de `requests.RequestException`.
10. Exibe um resumo da quantidade de URLs encontradas em cada categoria.

## 🎨 Cores no terminal

O projeto utiliza a biblioteca `colorama` para facilitar a visualização dos resultados:

| Status | Cor | Significado |
| --- | --- | --- |
| `200` | 🟢 Verde | Requisição realizada com sucesso |
| `404` | 🔴 Vermelho | Página não encontrada |
| Outros | 🟡 Amarelo | Outro código HTTP |

## ⚠️ Tratamento de erros

Caso uma URL não possa ser acessada, o programa não é interrompido. O erro é capturado e exibido no terminal:

```
Erro ao acessar https://exemplo.com: ...
```

 Isso permite que o processamento continue para as próximas URLs.

 ## 🔧 Melhorias futuras

 Algumas melhorias que podem ser implementadas:

- Adicionar `timeout` nas requisições.
- Verificar outros códigos HTTP, como `301`, `302`, `403` e `500`.
- Criar arquivos separados para cada status.
- Utilizar requisições paralelas para aumentar a velocidade.
- Adicionar argumentos de linha de comando.
- Permitir escolher o arquivo de entrada.
- Gerar um relatório final em CSV.
- Registrar erros em um arquivo de log.
- Adicionar testes automatizados.
- Utilizar `Session` do `requests` para reutilizar conexões.

 ## 📄 Licença

 Este projeto pode ser utilizado, modificado e distribuído livremente, caso nenhuma licença específica seja definida pelo autor.

---

 Desenvolvido em **Python** 

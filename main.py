import csv
import os
import time
import requests

from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from colorama import Fore, Style, init


# ============================================================
# CONFIGURAÇÕES
# ============================================================

ARQUIVO_ENTRADA = "base/2024/rj.txt"
ARQUIVO_SAIDA = "resultado/resultados.csv"

# Número máximo de threads concorrentes
MAX_WORKERS = 10  

# Timeout:
# (tempo para conectar, tempo máximo esperando resposta)
TIMEOUT = (5, 15)

# Quantidade de tentativas adicionais
RETRY_TOTAL = 3

# Status que podem ser repetidos automaticamente
RETRY_STATUS_CODES = [429, 500, 502, 503, 504]

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/140.0 Safari/537.36"
)


# Inicializa Colorama
init(autoreset=True)

# Garante que o diretório de saída exista
os.makedirs(os.path.dirname(ARQUIVO_SAIDA), exist_ok=True)


# ============================================================
# SESSION
# ============================================================

def criar_session():
    """
    Cria uma Session configurada com retry automático.
    """

    session = requests.Session()

    retry = Retry(
        total=RETRY_TOTAL,
        connect=RETRY_TOTAL,
        read=RETRY_TOTAL,
        status=RETRY_TOTAL,

        backoff_factor=1,

        status_forcelist=RETRY_STATUS_CODES,

        allowed_methods=[
            "GET",
            "HEAD"
        ],

        raise_on_status=False,
    )

    adapter = HTTPAdapter(
        max_retries=retry,
        pool_connections=MAX_WORKERS,
        pool_maxsize=MAX_WORKERS
    )

    session.mount("http://", adapter)
    session.mount("https://", adapter)

    session.headers.update({
        "User-Agent": USER_AGENT
    })

    return session


# ============================================================
# TESTE DE UMA URL
# ============================================================

def verificar_url(url):
    """
    Verifica uma URL e retorna um dicionário com o resultado.
    """

    inicio = time.perf_counter()

    # Cada worker terá sua própria Session
    session = criar_session()

    try:
        response = session.get(
            url,
            timeout=TIMEOUT,
            allow_redirects=True
        )

        tempo = time.perf_counter() - inicio

        return {
            "url": url,
            "status_code": response.status_code,
            "final_url": response.url,
            "tempo": round(tempo, 3),
            "erro": ""
        }

    except requests.Timeout as e:

        tempo = time.perf_counter() - inicio

        return {
            "url": url,
            "status_code": "",
            "final_url": "",
            "tempo": round(tempo, 3),
            "erro": f"TIMEOUT: {e}"
        }

    except requests.RequestException as e:

        tempo = time.perf_counter() - inicio

        return {
            "url": url,
            "status_code": "",
            "final_url": "",
            "tempo": round(tempo, 3),
            "erro": str(e)
        }

    finally:
        session.close()


# ============================================================
# BARRA DE PROGRESSO
# ============================================================

def mostrar_progresso(concluidas, total, inicio):
    """
    Mostra uma barra de progresso simples no terminal.
    """

    percentual = concluidas / total if total else 1

    largura = 40
    preenchido = int(largura * percentual)

    barra = (
        "=" * preenchido +
        "-" * (largura - preenchido)
    )

    tempo_decorrido = time.perf_counter() - inicio

    if concluidas:
        velocidade = concluidas / tempo_decorrido
        restante = (total - concluidas) / velocidade
    else:
        velocidade = 0
        restante = 0

    print(
        f"\r[{barra}] "
        f"{percentual:6.1%} "
        f"{concluidas}/{total} "
        f"| {velocidade:.1f} URLs/s "
        f"| ETA: {restante:.0f}s",
        end="",
        flush=True
    )


# ============================================================
# MAIN
# ============================================================

def main():

    # --------------------------------------------------------
    # Lê as URLs
    # --------------------------------------------------------

    with open(
        ARQUIVO_ENTRADA,
        "r",
        encoding="utf-8"
    ) as arquivo:

        urls = [
            linha.strip()
            for linha in arquivo
            if linha.strip()
        ]

    # Remove URLs duplicadas mantendo a ordem
    urls = list(dict.fromkeys(urls))

    total = len(urls)

    if total == 0:
        print("Nenhuma URL encontrada.")
        return

    print("=" * 70)
    print("URL CHECKER")
    print("=" * 70)

    print(f"URLs encontradas : {total}")
    print(f"Workers          : {MAX_WORKERS}")
    print(f"Timeout          : {TIMEOUT}")
    print(f"Retries          : {RETRY_TOTAL}")
    print("=" * 70)

    # --------------------------------------------------------
    # Contadores
    # --------------------------------------------------------

    contadores = {
        "200": 0,
        "3xx": 0,
        "404": 0,
        "4xx": 0,
        "5xx": 0,
        "erro": 0
    }

    resultados = []

    inicio = time.perf_counter()

    # --------------------------------------------------------
    # Execução concorrente
    # --------------------------------------------------------

    with ThreadPoolExecutor(
        max_workers=MAX_WORKERS
    ) as executor:

        futures = {
            executor.submit(verificar_url, url): url
            for url in urls
        }

        concluidas = 0

        for future in as_completed(futures):

            resultado = future.result()

            resultados.append(resultado)

            status = resultado["status_code"]

            # -----------------------------------------------
            # Classifica resultado
            # -----------------------------------------------

            if status == 200:

                contadores["200"] += 1

                print(
                    f"\n{Fore.GREEN}[200]{Style.RESET_ALL} "
                    f"{resultado['url']}"
                )

            elif status == 404:

                contadores["404"] += 1

                print(
                    f"\n{Fore.RED}[404]{Style.RESET_ALL} "
                    f"{resultado['url']}"
                )

            elif isinstance(status, int) and 300 <= status < 400:

                contadores["3xx"] += 1

                print(
                    f"\n{Fore.YELLOW}[{status}]{Style.RESET_ALL} "
                    f"{resultado['url']}"
                )

            elif isinstance(status, int) and 400 <= status < 500:

                contadores["4xx"] += 1

                print(
                    f"\n{Fore.YELLOW}[{status}]{Style.RESET_ALL} "
                    f"{resultado['url']}"
                )

            elif isinstance(status, int) and 500 <= status < 600:

                contadores["5xx"] += 1

                print(
                    f"\n{Fore.RED}[{status}]{Style.RESET_ALL} "
                    f"{resultado['url']}"
                )

            else:

                contadores["erro"] += 1

                print(
                    f"\n{Fore.RED}[ERRO]{Style.RESET_ALL} "
                    f"{resultado['url']} "
                    f"→ {resultado['erro']}"
                )

            # -----------------------------------------------
            # Atualiza progresso
            # -----------------------------------------------

            concluidas += 1

            mostrar_progresso(
                concluidas,
                total,
                inicio
            )

    print("\n")

    # --------------------------------------------------------
    # Ordena resultados pela URL
    # --------------------------------------------------------

    resultados.sort(
        key=lambda x: x["url"]
    )

    # --------------------------------------------------------
    # Salva CSV
    # --------------------------------------------------------

    with open(
        ARQUIVO_SAIDA,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as arquivo:

        campos = [
            "url",
            "status_code",
            "final_url",
            "tempo",
            "erro"
        ]

        writer = csv.DictWriter(
            arquivo,
            fieldnames=campos
        )

        writer.writeheader()

        writer.writerows(resultados)

    # --------------------------------------------------------
    # Resultado final
    # --------------------------------------------------------

    tempo_total = time.perf_counter() - inicio

    print("=" * 70)
    print("RESULTADO")
    print("=" * 70)

    print(f"Total de URLs : {total}")
    print(f"Status 200    : {contadores['200']}")
    print(f"Status 3xx    : {contadores['3xx']}")
    print(f"Status 404    : {contadores['404']}")
    print(f"Status 4xx    : {contadores['4xx']}")
    print(f"Status 5xx    : {contadores['5xx']}")
    print(f"Erros         : {contadores['erro']}")

    print("-" * 70)

    print(
        f"Tempo total   : {tempo_total:.2f}s"
    )

    print(
        f"Velocidade    : {total / tempo_total:.2f} URLs/s"
    )

    print(
        f"CSV salvo em  : {ARQUIVO_SAIDA}"
    )

    print("=" * 70)


if __name__ == "__main__":
    main()

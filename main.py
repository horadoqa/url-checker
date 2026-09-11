import os
import requests
from colorama import Fore, Style, init

init(autoreset=True)

ARQUIVO_ENTRADA = "base/2024/rj.txt"
ARQUIVO_200 = "resultado/200.csv"
ARQUIVO_404 = "resultado/404.csv"

TIMEOUT = 10

# Garante que o diretório de saída exista
os.makedirs("resultado", exist_ok=True)

contadores = {
    200: 0,
    404: 0,
    "outros": 0,
    "erros": 0
}

headers = {
    "User-Agent": "Mozilla/5.0 (URL Checker)"
}

with (
    open(ARQUIVO_ENTRADA, "r", encoding="utf-8") as entrada,
    open(ARQUIVO_200, "w", encoding="utf-8") as arq_200,
    open(ARQUIVO_404, "w", encoding="utf-8") as arq_404,
    requests.Session() as session
):

    session.headers.update(headers)

    for linha in entrada:
        url = linha.strip()

        if not url:
            continue

        print(f"Testando: {url}")

        try:
            response = session.get(
                url,
                timeout=TIMEOUT,
                allow_redirects=True
            )

            status = response.status_code

            if status == 200:
                print(
                    Fore.GREEN +
                    "STATUS CODE 200" +
                    Style.RESET_ALL
                )

                arq_200.write(url + "\n")
                contadores[200] += 1

            elif status == 404:
                print(
                    Fore.RED +
                    "STATUS CODE 404" +
                    Style.RESET_ALL
                )

                arq_404.write(url + "\n")
                contadores[404] += 1

            else:
                print(
                    Fore.YELLOW +
                    f"STATUS CODE {status}" +
                    Style.RESET_ALL
                )

                contadores["outros"] += 1

        except requests.Timeout:
            print(
                Fore.RED +
                "TIMEOUT" +
                Style.RESET_ALL
            )
            contadores["erros"] += 1

        except requests.RequestException as e:
            print(
                Fore.RED +
                f"ERRO: {e}" +
                Style.RESET_ALL
            )
            contadores["erros"] += 1


print("\n" + "-" * 50)
print("RESULTADO")
print("-" * 50)

print(f"URLs com status 200: {contadores[200]}")
print(f"URLs com status 404: {contadores[404]}")
print(f"URLs com outros status: {contadores['outros']}")
print(f"URLs com erro: {contadores['erros']}")

print("-" * 50)

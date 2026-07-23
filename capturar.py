import json
from playwright.sync_api import sync_playwright


def capturar_partidos_live():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                " (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1280, "height": 720},
        )
        page = context.new_page()

        datos_capturados = []

        def interceptar_respuesta(response):
            if "/api/matches/live" in response.url:
                print(f"Petición detectada: {response.url}")
                try:
                    json_data = response.json()
                    datos_capturados.append(json_data)
                except Exception as e:
                    print(f"Error al procesar JSON: {e}")

        page.on("response", interceptar_respuesta)

        print("Accediendo a la página...")
        page.goto("https://www.dataredonda.com/", wait_until="networkidle")

        if datos_capturados:
            with open("partidos_live.json", "w", encoding="utf-8") as f:
                json.dump(datos_capturados[0], f, ensure_ascii=False, indent=2)
            print("Datos guardados con éxito en partidos_live.json")
        else:
            print("No se encontró la petición /api/matches/live")

        browser.close()


if __name__ == "__main__":
    capturar_partidos_live()

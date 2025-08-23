import time
import pandas as pd
import yaml
from utils.scrapers_factory import ScrapterFactory


def load_config(path="configs/config.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_results(filename, new_results):
    """Concatena novos resultados SEM remover duplicatas."""
    df_new = pd.DataFrame(new_results)
    if df_new.empty:
        return

    try:
        df_old = pd.read_csv(filename)
    except FileNotFoundError:
        df_old = pd.DataFrame()

    df = pd.concat([df_old, df_new], ignore_index=True)
    df.to_csv(filename, index=False)
    print(f"📂 Arquivo atualizado: {filename} ({len(df)} linhas no total)")


def run_all_scrapers(config_path="configs/config.yaml"):
    config = load_config(config_path)

    repos = config["repos"]
    terms = config["terms"]
    max_pages = config["max_pages"]
    csv_filename = config["csv_filename"]

    all_results = []

    for repo_name, scraper_key in repos.items():
        print(f"\n🔍 Rodando scraper: {repo_name}")
        scraper = ScrapterFactory.get_scraper(scraper_key)

        for term in terms:
            try:
                results = scraper.search(term, max_pages)
                if results:
                    for r in results:
                        r["fonte"] = repo_name
                        r["termo"] = term
                    all_results.extend(results)
                    print(f"   ➕ {len(results)} resultados para '{term}'")
                else:
                    print(f"   ⚠️ Nenhum resultado para '{term}'")
            except Exception as e:
                print(f"   ❌ Erro no scraper {repo_name}: {e}")

        # Pausa para evitar requisições seguidas
        time.sleep(2)

    if all_results:
        save_results(csv_filename, all_results)


if __name__ == "__main__":
    run_all_scrapers()

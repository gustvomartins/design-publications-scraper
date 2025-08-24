"""
Pipeline principal para scraping de publicações de design.
Este módulo fornece uma interface unificada para executar o pipeline automatizado.
"""

from .automated_pipeline import AutomatedPipeline, run_automated_pipeline


class Pipeline:
    """Classe principal do pipeline de scraping"""
    
    def __init__(self, config_path="src/design_scraper/config/config.yaml"):
        self.config_path = config_path
        self.automated_pipeline = AutomatedPipeline(config_path)
    
    def run(self):
        """Executa o pipeline completo"""
        return self.automated_pipeline.run()
    
    def get_status(self):
        """Retorna o status atual do pipeline"""
        return self.automated_pipeline.get_status()


# Funções de conveniência para compatibilidade
def run_all_scrapers(config_path="src/design_scraper/config/config.yaml"):
    """Função de conveniência para executar o pipeline completo"""
    return run_automated_pipeline(config_path)


if __name__ == "__main__":
    # Execução direta do pipeline
    pipeline = Pipeline()
    result = pipeline.run()
    
    if result:
        print(f"\n✅ Pipeline executado com sucesso!")
        print(f"📊 Resumo: {result}")
    else:
        print(f"\n❌ Pipeline falhou!")

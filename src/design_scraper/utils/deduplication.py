import pandas as pd
import os
from datetime import datetime


class Deduplicator:
    """Classe para deduplicação de resultados de scraping"""
    
    def __init__(self, base_db_path="data/raw/base_database.csv"):
        self.base_db_path = base_db_path
        self.base_df = self._load_base_database()
    
    def _load_base_database(self):
        """Carrega a base de dados existente"""
        try:
            if os.path.exists(self.base_db_path):
                df = pd.read_csv(self.base_db_path)
                print(f"📚 Base de dados carregada: {len(df)} registros existentes")
                return df
            else:
                print(f"⚠️ Base de dados não encontrada em: {self.base_db_path}")
                return pd.DataFrame()
        except Exception as e:
            print(f"❌ Erro ao carregar base de dados: {e}")
            return pd.DataFrame()
    
    def find_new_records(self, filtered_results_path, output_path=None):
        """
        Encontra registros novos comparando com a base existente
        
        Args:
            filtered_results_path: Caminho para o CSV com resultados filtrados
            output_path: Caminho para salvar apenas os novos registros
        
        Returns:
            DataFrame com apenas os registros novos
        """
        try:
            # Carrega resultados filtrados
            filtered_df = pd.read_csv(filtered_results_path)
            print(f"🔍 Analisando {len(filtered_df)} resultados filtrados...")
            
            if self.base_df.empty:
                print("✅ Base de dados vazia - todos os registros são novos")
                new_records = filtered_df
            else:
                # Remove duplicatas baseado no campo 'link'
                new_records = self._remove_duplicates(filtered_df)
                print(f"✅ {len(new_records)} registros novos encontrados")
            
            # Salva apenas os novos registros
            if output_path:
                self._save_new_records(new_records, output_path)
            
            return new_records
            
        except Exception as e:
            print(f"❌ Erro na deduplicação: {e}")
            return pd.DataFrame()
    
    def _remove_duplicates(self, filtered_df):
        """Remove registros duplicados baseado no campo 'link'"""
        if 'link' not in filtered_df.columns:
            print("⚠️ Campo 'link' não encontrado - usando todos os registros")
            return filtered_df
        
        # Combina base existente com novos resultados
        combined_df = pd.concat([self.base_df, filtered_df], ignore_index=True)
        
        # Remove duplicatas baseado no link
        deduplicated_df = combined_df.drop_duplicates(subset=['link'], keep='first')
        
        # Filtra apenas os registros que estavam nos novos resultados
        new_records = deduplicated_df.iloc[len(self.base_df):]
        
        return new_records
    
    def _save_new_records(self, new_records, output_path):
        """Salva apenas os novos registros em um arquivo separado"""
        try:
            # Cria diretório se não existir
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Salva novos registros
            new_records.to_csv(output_path, index=False)
            print(f"💾 Novos registros salvos em: {output_path}")
            print(f"   📊 Total de novos registros: {len(new_records)}")
            
            # IMPORTANTE: NÃO atualiza a base de dados automaticamente
            # Os novos registros são salvos separadamente para revisão manual
            print("ℹ️ Base de dados NÃO foi atualizada automaticamente")
            print("   Os novos registros foram salvos separadamente para revisão")
            
        except Exception as e:
            print(f"❌ Erro ao salvar novos registros: {e}")
    
    def get_statistics(self):
        """Retorna estatísticas da base de dados"""
        if self.base_df.empty:
            return {"total_records": 0, "unique_sources": 0, "unique_terms": 0}
        
        stats = {
            "total_records": len(self.base_df),
            "unique_sources": self.base_df['database'].nunique() if 'database' in self.base_df.columns else 0,
            "unique_terms": self.base_df['category'].nunique() if 'category' in self.base_df.columns else 0
        }
        
        return stats
    
    def get_new_records_summary(self, new_records_df):
        """Retorna resumo dos novos registros encontrados"""
        if new_records_df.empty:
            return "Nenhum registro novo encontrado"
        
        summary = f"📋 Resumo dos {len(new_records_df)} novos registros:\n"
        
        # Contagem por fonte/database
        if 'database' in new_records_df.columns:
            source_counts = new_records_df['database'].value_counts()
            summary += "\n📚 Por fonte:\n"
            for source, count in source_counts.items():
                summary += f"   • {source}: {count}\n"
        
        # Contagem por categoria
        if 'category' in new_records_df.columns:
            category_counts = new_records_df['category'].value_counts()
            summary += "\n🏷️ Por categoria:\n"
            for category, count in category_counts.items():
                summary += f"   • {category}: {count}\n"
        
        return summary


def run_deduplication(filtered_results_path, base_db_path="data/raw/base_database.csv", 
                     output_path="data/processed/new_records.csv"):
    """
    Função principal para executar a deduplicação
    
    Args:
        filtered_results_path: Caminho para o CSV com resultados filtrados
        base_db_path: Caminho para a base de dados existente
        output_path: Caminho para salvar apenas os novos registros
    """
    print("🔄 Iniciando processo de deduplicação...")
    
    deduplicator = Deduplicator(base_db_path)
    
    # Executa deduplicação
    new_records = deduplicator.find_new_records(filtered_results_path, output_path)
    
    # Mostra estatísticas da base
    base_stats = deduplicator.get_statistics()
    print(f"\n📊 Estatísticas da base de dados:")
    print(f"   Total de registros: {base_stats['total_records']}")
    print(f"   Fontes únicas: {base_stats['unique_sources']}")
    print(f"   Categorias únicas: {base_stats['unique_terms']}")
    
    if not new_records.empty:
        print(f"\n✨ Deduplicação concluída!")
        print(f"   Novos registros: {len(new_records)}")
        print(f"   Arquivo salvo em: {output_path}")
        
        # Mostra resumo dos novos registros
        summary = deduplicator.get_new_records_summary(new_records)
        print(f"\n{summary}")
        
        print(f"\n⚠️ IMPORTANTE:")
        print(f"   • A base de dados NÃO foi atualizada automaticamente")
        print(f"   • Os novos registros foram salvos em: {output_path}")
        print(f"   • Revise os registros antes de adicionar à base principal")
        
    else:
        print(f"\n✨ Nenhum registro novo encontrado!")
    
    return new_records


if __name__ == "__main__":
    # Exemplo de uso
    run_deduplication("data/processed/filtered_results.csv")

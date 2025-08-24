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
    
    def find_new_records(self, new_results_path, output_path=None):
        """
        Encontra registros novos comparando com a base existente
        
        Args:
            new_results_path: Caminho para o CSV com novos resultados
            output_path: Caminho para salvar apenas os novos registros
        
        Returns:
            DataFrame com apenas os registros novos
        """
        try:
            # Carrega novos resultados
            new_df = pd.read_csv(new_results_path)
            print(f"🔍 Analisando {len(new_df)} novos resultados...")
            
            if self.base_df.empty:
                print("✅ Base de dados vazia - todos os registros são novos")
                new_records = new_df
            else:
                # Remove duplicatas baseado no campo 'link'
                new_records = self._remove_duplicates(new_df)
                print(f"✅ {len(new_records)} registros novos encontrados")
            
            # Salva apenas os novos registros
            if output_path:
                self._save_new_records(new_records, output_path)
            
            return new_records
            
        except Exception as e:
            print(f"❌ Erro na deduplicação: {e}")
            return pd.DataFrame()
    
    def _remove_duplicates(self, new_df):
        """Remove registros duplicados baseado no campo 'link'"""
        if 'link' not in new_df.columns:
            print("⚠️ Campo 'link' não encontrado - usando todos os registros")
            return new_df
        
        # Combina base existente com novos resultados
        combined_df = pd.concat([self.base_df, new_df], ignore_index=True)
        
        # Remove duplicatas baseado no link
        deduplicated_df = combined_df.drop_duplicates(subset=['link'], keep='first')
        
        # Filtra apenas os registros que estavam nos novos resultados
        new_records = deduplicated_df.iloc[len(self.base_df):]
        
        return new_records
    
    def _save_new_records(self, new_records, output_path):
        """Salva apenas os registros novos em um arquivo separado"""
        try:
            # Cria diretório se não existir
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Salva novos registros
            new_records.to_csv(output_path, index=False)
            print(f"💾 Novos registros salvos em: {output_path}")
            
            # Atualiza a base de dados com todos os registros
            self._update_base_database(new_records)
            
        except Exception as e:
            print(f"❌ Erro ao salvar novos registros: {e}")
    
    def _update_base_database(self, new_records):
        """Atualiza a base de dados com os novos registros"""
        try:
            # Combina base existente com novos registros
            updated_base = pd.concat([self.base_df, new_records], ignore_index=True)
            
            # Remove duplicatas finais
            updated_base = updated_base.drop_duplicates(subset=['link'], keep='first')
            
            # Salva base atualizada
            updated_base.to_csv(self.base_db_path, index=False)
            print(f"🔄 Base de dados atualizada: {len(updated_base)} registros totais")
            
            # Atualiza o DataFrame interno
            self.base_df = updated_base
            
        except Exception as e:
            print(f"❌ Erro ao atualizar base de dados: {e}")
    
    def get_statistics(self):
        """Retorna estatísticas da base de dados"""
        if self.base_df.empty:
            return {"total_records": 0, "unique_sources": 0, "unique_terms": 0}
        
        stats = {
            "total_records": len(self.base_df),
            "unique_sources": self.base_df['fonte'].nunique() if 'fonte' in self.base_df.columns else 0,
            "unique_terms": self.base_df['termo'].nunique() if 'termo' in self.base_df.columns else 0
        }
        
        return stats


def run_deduplication(new_results_path, base_db_path="data/raw/base_database.csv", 
                     output_path="data/processed/new_records.csv"):
    """
    Função principal para executar a deduplicação
    
    Args:
        new_results_path: Caminho para o CSV com novos resultados
        base_db_path: Caminho para a base de dados existente
        output_path: Caminho para salvar apenas os novos registros
    """
    print("🔄 Iniciando processo de deduplicação...")
    
    deduplicator = Deduplicator(base_db_path)
    
    # Executa deduplicação
    new_records = deduplicator.find_new_records(new_results_path, output_path)
    
    # Mostra estatísticas
    stats = deduplicator.get_statistics()
    print(f"\n📊 Estatísticas da base de dados:")
    print(f"   Total de registros: {stats['total_records']}")
    print(f"   Fontes únicas: {stats['unique_sources']}")
    print(f"   Termos únicos: {stats['unique_terms']}")
    
    if not new_records.empty:
        print(f"\n✨ Deduplicação concluída!")
        print(f"   Novos registros: {len(new_records)}")
        print(f"   Arquivo salvo em: {output_path}")
    else:
        print(f"\n✨ Nenhum registro novo encontrado!")
    
    return new_records


if __name__ == "__main__":
    # Exemplo de uso
    run_deduplication("data/raw/search_results.csv")

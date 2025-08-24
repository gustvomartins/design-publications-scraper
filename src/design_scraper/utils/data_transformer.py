import pandas as pd
import uuid
from datetime import datetime
import re
import os


class DataTransformer:
    """Transforma dados de resultados de busca para o formato da base de dados"""
    
    def __init__(self):
        self.base_columns = [
            'id', 'timestamp', 'title', 'author', 'year', 'type', 
            'link', 'database', 'category', 'cover_image', '🔐 Softr Record ID'
        ]
    
    def transform_search_results(self, search_results_df):
        """
        Transforma resultados de busca para o formato da base de dados
        
        Args:
            search_results_df: DataFrame com resultados de busca
            
        Returns:
            DataFrame transformado com estrutura da base de dados
        """
        if search_results_df.empty:
            return pd.DataFrame(columns=self.base_columns)
        
        # Cria DataFrame transformado
        transformed_data = []
        
        for _, row in search_results_df.iterrows():
            transformed_row = self._transform_single_record(row)
            if transformed_row:
                transformed_data.append(transformed_row)
        
        # Cria DataFrame final
        transformed_df = pd.DataFrame(transformed_data, columns=self.base_columns)
        
        # Define tipos de dados explícitos para evitar conversão automática
        transformed_df = transformed_df.astype({
            'id': 'string',
            'timestamp': 'string',
            'title': 'string',
            'author': 'string',
            'year': 'string',
            'type': 'string',
            'link': 'string',
            'database': 'string',
            'category': 'string',
            'cover_image': 'string',
            '🔐 Softr Record ID': 'string'
        })
        
        print(f"🔄 Transformados {len(transformed_df)} registros para o formato da base de dados")
        return transformed_df
    
    def _transform_single_record(self, row):
        """Transforma um único registro"""
        try:
            # Extrai ano da data ou edição
            year = self._extract_year(row)
            
            # Determina o tipo baseado no conteúdo
            pub_type = self._determine_publication_type(row)
            
            # Determina a categoria baseada no termo de busca
            category = self._determine_category(row.get('termo', ''))
            
            # Determina o database baseado na fonte
            database = self._determine_database(row.get('fonte', ''))
            
            transformed_record = {
                'id': str(uuid.uuid4()),
                'timestamp': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                'title': self._clean_text(row.get('title', '')),
                'author': self._clean_text(row.get('author', '')),
                'year': year if year else 'Sem ano',
                'type': pub_type,
                'link': row.get('link', ''),
                'database': database,
                'category': category,
                'cover_image': 'Sem imagem',  # Não disponível nos resultados de busca
                '🔐 Softr Record ID': 'Sem ID'  # Será preenchido posteriormente se necessário
            }
            
            return transformed_record
            
        except Exception as e:
            print(f"⚠️ Erro ao transformar registro: {e}")
            return None
    
    def _extract_year(self, row):
        """Extrai ano de uma linha de dados, verificando tanto date quanto edition"""
        # Verifica o campo date primeiro
        date_str = row.get('date', '')
        if not pd.isna(date_str) and date_str != '' and date_str != 'Data não informada':
            year = self._extract_year_from_string(str(date_str))
            if year:
                return year
        
        # Se não encontrou no date, verifica o campo edition
        edition_str = row.get('edition', '')
        if not pd.isna(edition_str) and edition_str != '':
            year = self._extract_year_from_string(str(edition_str))
            if year:
                return year
        
        return ''
    
    def _extract_year_from_string(self, date_str):
        """Extrai ano de uma string específica"""
        if not date_str or date_str == '':
            return ''
        
        # Procura por padrões de ano (4 dígitos)
        year_match = re.search(r'\b(19|20)\d{2}\b', date_str)
        if year_match:
            return year_match.group()
        
        # Procura por padrões de edição (ex: v. 31, n. 3 (2023))
        edition_match = re.search(r'\((\d{4})\)', date_str)
        if edition_match:
            return edition_match.group(1)
        
        # Procura por padrões de data (ex: 16-05-2018, 2022-04-04)
        date_patterns = [
            r'(\d{4})-\d{2}-\d{2}',  # YYYY-MM-DD
            r'\d{2}-\d{2}-(\d{4})',  # DD-MM-YYYY
            r'(\d{4})-\d{2}',         # YYYY-MM
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, date_str)
            if match:
                return match.group(1)
        
        return ''
    
    def _determine_publication_type(self, row):
        """Determina o tipo de publicação baseado no conteúdo"""
        title = str(row.get('title', '')).lower()
        fonte = str(row.get('fonte', '')).lower()
        
        # Verifica se é um artigo baseado na fonte ou título
        if any(journal in fonte for journal in ['revista', 'journal', 'estudos', 'infodesign', 'human factors', 'arcos', 'triades', 'educacao grafica']):
            return 'Artigo'
        
        # Verifica se é um livro baseado no título
        if any(word in title for word in ['livro', 'book', 'manual', 'guia']):
            return 'Livro'
        
        # Padrão: se tem link para PDF ou resumo, provavelmente é artigo
        if row.get('pdf_link') or row.get('resumo_link'):
            return 'Artigo'
        
        # Padrão: se tem edition_link, provavelmente é artigo
        if row.get('edition_link'):
            return 'Artigo'
        
        return 'Artigo'  # Padrão para resultados de busca
    
    def _determine_category(self, search_term):
        """Determina categoria baseada no termo de busca"""
        term = str(search_term).lower()
        
        category_mapping = {
            'experiencia': 'Fundamentos',
            'usuario': 'Fundamentos',
            'interface': 'Visual',
            'usabilidade': 'Fundamentos',
            'interacao': 'Fundamentos',
            'sistema': 'Tecnologia',
            'ergonomia': 'Fundamentos',
            'digital': 'Tecnologia',
            'informacao': 'Informação',
            'tecnologia': 'Tecnologia',
            'inteligencia artificial': 'Tecnologia',
            'design thinking': 'Processos',
            'ux': 'Fundamentos'
        }
        
        for key, category in category_mapping.items():
            if key in term:
                return category
        
        return 'Fundamentos'  # Categoria padrão
    
    def _determine_database(self, fonte):
        """Determina o nome do database baseado na fonte"""
        # Verifica se a fonte é válida
        if pd.isna(fonte) or fonte == '':
            return 'Fonte não informada'
        
        fonte_lower = str(fonte).lower()
        
        database_mapping = {
            'estudos em design': 'Revista Estudos em Design',
            'infodesign': 'InfoDesign',
            'human factors in design': 'Human Factors in Design',
            'arcos design': 'Arcos Design',
            'design e tecnologia': 'Design e Tecnologia',
            'triades': 'Tríades em Revista',
            'educacao grafica': 'Educação Gráfica'
        }
        
        for key, database in database_mapping.items():
            if key in fonte_lower:
                return database
        
        return fonte  # Retorna a fonte original se não encontrar mapeamento
    
    def _clean_text(self, text):
        """Limpa e normaliza texto"""
        if pd.isna(text) or text == '':
            return ''
        
        # Remove aspas extras e normaliza
        cleaned = str(text).strip()
        cleaned = cleaned.replace('"', '').replace('"', '').replace('"', '')
        
        return cleaned
    
    def validate_transformation(self, transformed_df):
        """Valida se a transformação foi bem-sucedida"""
        if transformed_df.empty:
            return False, "DataFrame vazio"
        
        # Verifica se todas as colunas necessárias estão presentes
        missing_columns = set(self.base_columns) - set(transformed_df.columns)
        if missing_columns:
            return False, f"Colunas faltando: {missing_columns}"
        
        # Verifica se há dados válidos
        if transformed_df['title'].isna().all() or transformed_df['link'].isna().all():
            return False, "Dados essenciais (título ou link) estão vazios"
        
        return True, "Transformação válida"
    
    def get_transformation_stats(self, original_df, transformed_df):
        """Retorna estatísticas da transformação"""
        stats = {
            'original_records': len(original_df),
            'transformed_records': len(transformed_df),
            'success_rate': len(transformed_df) / len(original_df) * 100 if len(original_df) > 0 else 0,
            'missing_data': len(original_df) - len(transformed_df)
        }
        
        return stats


def transform_and_save_results(search_results_path, output_path, base_db_path=None):
    """
    Função principal para transformar e salvar resultados
    
    Args:
        search_results_path: Caminho para CSV com resultados de busca
        output_path: Caminho para salvar resultados transformados
        base_db_path: Caminho opcional para base de dados existente
    """
    print("🔄 Iniciando transformação de dados...")
    
    try:
        # Carrega resultados de busca
        search_df = pd.read_csv(search_results_path)
        print(f"📖 Carregados {len(search_df)} resultados de busca")
        
        # Transforma dados
        transformer = DataTransformer()
        transformed_df = transformer.transform_search_results(search_df)
        
        if transformed_df.empty:
            print("⚠️ Nenhum dado foi transformado")
            return None
        
        # Valida transformação
        is_valid, message = transformer.validate_transformation(transformed_df)
        if not is_valid:
            print(f"❌ Validação falhou: {message}")
            return None
        
        # Salva resultados transformados
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Salva com tipos de dados preservados
        transformed_df.to_csv(output_path, index=False)
        
        # Verifica se os dados foram salvos corretamente
        verification_df = pd.read_csv(output_path)
        print(f"💾 Resultados transformados salvos em: {output_path}")
        print(f"   Verificação: {len(verification_df)} registros salvos")
        
        # Mostra estatísticas
        stats = transformer.get_transformation_stats(search_df, transformed_df)
        print(f"\n📊 Estatísticas da transformação:")
        print(f"   Registros originais: {stats['original_records']}")
        print(f"   Registros transformados: {stats['transformed_records']}")
        print(f"   Taxa de sucesso: {stats['success_rate']:.1f}%")
        print(f"   Dados perdidos: {stats['missing_data']}")
        
        return transformed_df
        
    except Exception as e:
        print(f"❌ Erro na transformação: {e}")
        return None


if __name__ == "__main__":
    # Exemplo de uso
    transform_and_save_results(
        "data/raw/search_results.csv",
        "data/processed/transformed_results.csv"
    )

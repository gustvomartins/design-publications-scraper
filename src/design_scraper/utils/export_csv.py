import csv 

class CSVExporter:
    """Classe para exportação de dados para CSV"""
    
    @staticmethod
    def export_to_csv(filename, data, fieldnames):
        """Exporta dados para arquivo CSV"""
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)


def export_to_csv(filename, data, fieldnames):
    """Função de conveniência para exportação CSV"""
    CSVExporter.export_to_csv(filename, data, fieldnames)
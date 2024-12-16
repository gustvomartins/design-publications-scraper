### README.md

```markdown
# Academic Publication Scraper API

A Python-based API for querying and extracting information about academic publications from repositories and journals. This tool is designed to help researchers and developers streamline the process of finding and organizing academic content.

## Features
- Scrapes academic repositories for publication details.
- Retrieves publication titles, authors, publication dates, and URLs.
- Supports pagination for large queries.
- Exports results to a CSV file for easy analysis and sharing.

## Requirements
- Python 3.7 or higher
- The following Python libraries:
  - `requests`
  - `beautifulsoup4`

Install the required libraries using:
```bash
pip install requests beautifulsoup4
```

## How to Use
1. Clone this repository:
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. Run the script:
   ```bash
   python scraper.py
   ```

3. Enter the search term and the number of pages you want to scrape.

4. The results will be saved to a `search_results.csv` file in the same directory.

## Example
**Input:**  
```
Enter the search term: UX Design  
Enter the number of pages to scrape: 3  
```

**Output:**  
A `search_results.csv` file containing:
| title                     | author          | link                                      | date       |
|---------------------------|-----------------|-------------------------------------------|------------|
| UX Research in Practice   | John Doe        | https://repositorio.ufrn.br/123456        | 2023-05-01 |
| Interaction Design Basics | Jane Smith      | https://repositorio.ufrn.br/789012        | 2022-11-15 |

## Notes
- The script is configured to scrape the UFRN repository. Adjust the `base_url` variable in the code to target other repositories if needed.
- Ensure compliance with the repository's terms of service before using this tool.

## Contributing
Feel free to fork the repository and submit pull requests for improvements or additional features.

## License
This project is licensed under the MIT License.
```

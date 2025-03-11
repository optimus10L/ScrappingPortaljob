import requests
from bs4 import BeautifulSoup
import csv
import time
import random

def scrape_asako(url, pages=5):
    """
    Scrape les offres d'emploi depuis Asako Madagascar
    """
    all_jobs = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Parcourir plusieurs pages
    for page in range(1, pages + 1):
        # Construire l'URL de pagination
        if page == 1:
            page_url = url
        else:
            page_url = f"{url}page/{page}/"
        
        try:
            print(f"Scraping Asako page {page}...")
            response = requests.get(page_url, headers=headers)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Trouver tous les conteneurs d'offres d'emploi
                job_listings = soup.select('article.job_listing')
                
                if not job_listings:
                    print("Aucune offre trouvée sur cette page.")
                    break
                
                for job in job_listings:
                    job_data = {}
                    
                    # Titre du poste
                    title_element = job.select_one('h3.job_listing-title')
                    job_data['titre'] = title_element.text.strip() if title_element else "Non spécifié"
                    
                    # Entreprise
                    company_element = job.select_one('div.job_listing-company strong')
                    job_data['entreprise'] = company_element.text.strip() if company_element else "Non spécifié"
                    
                    # Lieu
                    location_element = job.select_one('div.location')
                    job_data['lieu'] = location_element.text.strip() if location_element else "Non spécifié"
                    
                    # Description courte
                    description_element = job.select_one('div.job_listing-description')
                    job_data['description'] = description_element.text.strip() if description_element else "Non spécifié"
                    
                    # Date de publication
                    date_element = job.select_one('time.job_listing-posted-time')
                    job_data['date_publication'] = date_element.text.strip() if date_element else "Non spécifié"
                    
                    # Lien de l'offre
                    job_link = job.select_one('a.job_listing-clickbox')
                    if job_link and 'href' in job_link.attrs:
                        job_data['lien'] = job_link['href']
                    else:
                        job_data['lien'] = "Non disponible"
                    
                    # Type de contrat
                    contract_element = job.select_one('div.job-type')
                    job_data['type_contrat'] = contract_element.text.strip() if contract_element else "Non spécifié"
                    
                    # Catégorie
                    category_element = job.select_one('div.job_listing-category')
                    job_data['categorie'] = category_element.text.strip() if category_element else "Non spécifié"
                    
                    all_jobs.append(job_data)
                
                # Pause pour éviter d'être bloqué
                time.sleep(random.uniform(2, 5))
            else:
                print(f"Erreur de requête: {response.status_code}")
                break
                
        except Exception as e:
            print(f"Erreur lors du scraping: {e}")
            break
    
    return all_jobs

def save_to_csv(jobs, filename):
    """
    Enregistre les offres d'emploi dans un fichier CSV
    """
    if not jobs:
        print(f"Aucune donnée à enregistrer dans {filename}")
        return
        
    fieldnames = ['titre', 'entreprise', 'lieu', 'description', 'date_publication', 'lien', 'type_contrat', 'categorie']
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for job in jobs:
            writer.writerow(job)
    
    print(f"{len(jobs)} offres enregistrées dans {filename}")

if __name__ == "__main__":
    asako_url = "https://www.asako.mg/"
    jobs = scrape_asako(asako_url, pages=5)
    save_to_csv(jobs, "asako_madagascar_jobs.csv")
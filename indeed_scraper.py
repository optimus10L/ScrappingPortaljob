import requests
from bs4 import BeautifulSoup
import csv
import time
import random

def scrape_indeed(url, pages=5):
    """
    Scrape les offres d'emploi depuis Indeed Madagascar
    """
    all_jobs = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Parcourir plusieurs pages
    for page in range(pages):
        # Construire l'URL de pagination
        if page == 0:
            page_url = url
        else:
            page_url = url.replace("?vjk=1ac7454d4117f55f", f"&start={page*10}&vjk=1ac7454d4117f55f")
        
        try:
            print(f"Scraping Indeed page {page+1}...")
            response = requests.get(page_url, headers=headers)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Trouver tous les conteneurs d'offres d'emploi
                job_listings = soup.select('div.job_seen_beacon')
                
                if not job_listings:
                    print("Aucune offre trouvée sur cette page.")
                    break
                
                for job in job_listings:
                    job_data = {}
                    
                    # Titre du poste
                    title_element = job.select_one('h2.jobTitle span[title]')
                    job_data['titre'] = title_element.get('title') if title_element else "Non spécifié"
                    
                    # Entreprise
                    company_element = job.select_one('span.companyName')
                    job_data['entreprise'] = company_element.text.strip() if company_element else "Non spécifié"
                    
                    # Lieu
                    location_element = job.select_one('div.companyLocation')
                    job_data['lieu'] = location_element.text.strip() if location_element else "Non spécifié"
                    
                    # Description
                    description_element = job.select_one('div.job-snippet')
                    job_data['description'] = description_element.text.strip() if description_element else "Non spécifié"
                    
                    # Date de publication
                    date_element = job.select_one('span.date')
                    job_data['date_publication'] = date_element.text.strip() if date_element else "Non spécifié"
                    
                    # Lien de l'offre
                    job_link = job.select_one('h2.jobTitle a')
                    if job_link and 'href' in job_link.attrs:
                        job_data['lien'] = "https://fr.indeed.com" + job_link['href']
                    else:
                        job_data['lien'] = "Non disponible"
                    
                    # Type de contrat (si disponible)
                    job_type_element = job.select_one('div.metadata span.attribute_snippet')
                    job_data['type_contrat'] = job_type_element.text.strip() if job_type_element else "Non spécifié"
                    
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
        
    fieldnames = ['titre', 'entreprise', 'lieu', 'description', 'date_publication', 'lien', 'type_contrat']
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for job in jobs:
            writer.writerow(job)
    
    print(f"{len(jobs)} offres enregistrées dans {filename}")

if __name__ == "__main__":
    indeed_url = "https://fr.indeed.com/q-madagascar-emplois.html?vjk=1ac7454d4117f55f"
    jobs = scrape_indeed(indeed_url, pages=5)
    save_to_csv(jobs, "indeed_madagascar_jobs.csv")
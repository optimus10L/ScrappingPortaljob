import requests
from bs4 import BeautifulSoup
import csv
import time
import random

def scrape_portaljob(url, pages=2):
    """
    Scrape les offres d'emploi depuis PortalJob Madagascar
    """
    all_jobs = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Parcourir plusieurs pages (ici limité à 2 pages)
    for page in range(1, pages + 1):
        
        page_url = f"https://www.portaljob-madagascar.com/emploi/liste/page:{page}"
        
        try:
            print(f"Scraping PortalJob page {page}...")
            response = requests.get(page_url, headers=headers)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Rechercher les annonces d'emploi
                job_listings = soup.select('.item_annonce')  
                
                if not job_listings:
                    print(f"Aucune offre trouvée sur la page {page}.")
                    break
                
                print(f"Nombre d'offres trouvées sur la page {page}: {len(job_listings)}")
                
                for job in job_listings:
                    job_data = {}
                    
                    # Titre de l'offre
                    title_element = job.select_one('.description')  # Classe pour le titre
                    if title_element:
                        job_data['titre'] = title_element.text.strip()
                    
                    # Lien de l'offre
                    job_link = job.select_one('a[href]')
                    if job_link:
                        job_data['lien'] = job_link['href']
                    
                    # Entreprise
                    company_element = job.select_one('.fa-building')  # Classe pour l'entreprise
                    if company_element:
                        job_data['entreprise'] = company_element.text.strip()
                    
                    # Lieu
                    location_element = job.select_one('.fa-map-marker')  # Classe pour le lieu
                    if location_element:
                        job_data['lieu'] = location_element.text.strip()
                    
                    # Description
                    description_element = job.select_one('.contenu_annonce')  # Classe pour la description
                    if description_element:
                        job_data['description'] = description_element.text.strip()
                    
                    # Date de publication
                    date_element = job.select_one('.date_annonce')  # Classe pour la date
                    if date_element:
                        job_data['date_publication'] = date_element.text.strip()
                    
                    # Type de contrat
                    contract_type_element = job.select_one('.type_contrat')  # Classe pour le type de contrat
                    if contract_type_element:
                        job_data['type_contrat'] = contract_type_element.text.strip()
                    
                    # Secteur d'activité
                    sector_element = job.select_one('.secteur')  # Classe pour le secteur d'activité
                    if sector_element:
                        job_data['secteur'] = sector_element.text.strip()
                    
                    # Expérience requise
                    experience_element = job.select_one('.experience')  # Classe pour l'expérience requise
                    if experience_element:
                        job_data['experience_requise'] = experience_element.text.strip()
                    
                    # Date d'expiration de l'offre
                    expiration_element = job.select_one('.date_expiration')  # Classe pour la date d'expiration
                    if expiration_element:
                        job_data['date_expiration'] = expiration_element.text.strip()
                    
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
    if not jobs:
        print(f"Aucune donnée à enregistrer dans {filename}")
        return
        
    fieldnames = ['titre', 'entreprise', 'lieu', 'description', 'date_publication', 'lien', 'type_contrat', 'secteur', 'experience_requise', 'date_expiration']
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for job in jobs:
            writer.writerow(job)
    
    print(f"{len(jobs)} offres enregistrées dans {filename}")

if __name__ == "__main__":
    portaljob_url = "https://www.portaljob-madagascar.com/emploi/liste"
    jobs = scrape_portaljob(portaljob_url, pages=2)  
    save_to_csv(jobs, "portaljob_madagascar_jobs.csv")

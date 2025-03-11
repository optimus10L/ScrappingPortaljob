import requests
from bs4 import BeautifulSoup
import csv
import time
import random
from datetime import datetime

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
        # Construire l'URL de pagination
        page_url = f"https://www.portaljob-madagascar.com/emploi/liste/page:{page}"
        
        try:
            print(f"Scraping PortalJob page {page}...")
            response = requests.get(page_url, headers=headers)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Rechercher les annonces d'emploi
                job_listings = soup.select('.item_annonce')  # Ajuster selon les classes trouvées
                
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

def sort_jobs_by_sector_and_date(jobs):
    """
    Trie les offres d'emploi par secteur et par date de publication (les plus récentes en premier)
    """
    # Créer un dictionnaire avec les secteurs comme clés et les offres comme valeurs
    jobs_by_sector = {}
    
    for job in jobs:
        sector = job.get('secteur', 'Non spécifié')  
        if sector not in jobs_by_sector:
            jobs_by_sector[sector] = []
        
        # Convertir la date de publication en format datetime pour le tri
        try:
            job['date_publication_dt'] = datetime.strptime(job['date_publication'], '%d-%m-%Y')  
        except ValueError:
            job['date_publication_dt'] = datetime.min  # Si la date est mal formatée ou manquante, utiliser une date très ancienne
        
        jobs_by_sector[sector].append(job)
    
    # Trier les offres par date (les plus récentes en premier) pour chaque secteur
    for sector, sector_jobs in jobs_by_sector.items():
        jobs_by_sector[sector] = sorted(sector_jobs, key=lambda x: x['date_publication_dt'], reverse=True)
    
    return jobs_by_sector

def save_to_csv(jobs_by_sector, filename):
    """
    Enregistre les offres d'emploi triées par secteur dans un fichier CSV
    """
    if not jobs_by_sector:
        print(f"Aucune donnée à enregistrer dans {filename}")
        return
    
    fieldnames = ['titre', 'entreprise', 'lieu', 'description', 'date_publication', 'lien', 'type_contrat', 'secteur', 'experience_requise', 'date_expiration']
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # Pour chaque secteur, écrire les offres triées
        for sector, sector_jobs in jobs_by_sector.items():
            for job in sector_jobs:
                # Supprimer la clé 'date_publication_dt' avant d'enregistrer
                if 'date_publication_dt' in job:
                    del job['date_publication_dt']
                writer.writerow(job)
    
    print(f"Offres enregistrées dans {filename}")


if __name__ == "__main__":
    portaljob_url = "https://www.portaljob-madagascar.com/emploi/liste"
    jobs = scrape_portaljob(portaljob_url, pages=2)  # Limité à 2 pages
    jobs_by_sector = sort_jobs_by_sector_and_date(jobs)
    save_to_csv(jobs_by_sector, "portaltest.csv")

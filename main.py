from indeed_scraper import scrape_indeed, save_to_csv as save_indeed
from portaljob_scraper import scrape_portaljob, save_to_csv as save_portaljob
from asako_scraper import scrape_asako, save_to_csv as save_asako

def main():
    """
    Script principal pour exécuter tous les scrapers de sites d'emploi
    """
    print("Démarrage du scraping des offres d'emploi à Madagascar...")
    
    # Nombre de pages à scraper pour chaque site
    pages = 5
    
    # Scraping de Indeed Madagascar
    print("\n--- Scraping de Indeed Madagascar ---")
    indeed_url = "https://fr.indeed.com/q-madagascar-emplois.html?vjk=1ac7454d4117f55f"
    indeed_jobs = scrape_indeed(indeed_url, pages)
    save_indeed(indeed_jobs, "indeed_madagascar_jobs.csv")
    
    # Scraping de PortalJob Madagascar
    print("\n--- Scraping de PortalJob Madagascar ---")
    portaljob_url = "https://www.portaljob-madagascar.com/emploi/liste"
    portaljob_jobs = scrape_portaljob(portaljob_url, pages)
    save_portaljob(portaljob_jobs, "portaljob_madagascar_jobs.csv")
    
    # Scraping de Asako Madagascar
    print("\n--- Scraping de Asako Madagascar ---")
    asako_url = "https://www.asako.mg/"
    asako_jobs = scrape_asako(asako_url, pages)
    save_asako(asako_jobs, "asako_madagascar_jobs.csv")
    
    print("\nScraping terminé. Les fichiers CSV ont été créés.")
    
    # Afficher le nombre total d'offres d'emploi
    total_jobs = len(indeed_jobs) + len(portaljob_jobs) + len(asako_jobs)
    print(f"Nombre total d'offres d'emploi récupérées: {total_jobs}")
    print(f"Indeed: {len(indeed_jobs)}")
    print(f"PortalJob: {len(portaljob_jobs)}")
    print(f"Asako: {len(asako_jobs)}")

if __name__ == "__main__":
    main()
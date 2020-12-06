import pkg_resources
from selenium import webdriver
from paperscraper import PaperScraper

scraper = PaperScraper(webdriver_path=pkg_resources.resource_filename('paperscraper', 'webdrivers/chromedriver.exe'))

print(scraper.extract_from_url('https://www.sciencedirect.com/science/article/pii/S1878535217300990'))
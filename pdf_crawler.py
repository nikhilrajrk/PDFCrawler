import os
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver

#Getting Book Name From User
book = input("Enter Book Name : ")

#Concate Pdfdrive and Book Name
search_url = 'https://www.pdfdrive.com/search?q='+book
url = 'https://www.pdfdrive.com'

#Getting Source Code from search_url
r = requests.get(search_url).content
soup = BeautifulSoup(r,'lxml')

#Filtering 'a' Tags
a_tag = soup.find_all('a',{"class":"ai-search"})

#All Download Links are appending into download_links
download_links = []

print("Please Wait Scarping All PDF Url...")

#Scraping All PDF Links
def pdf_download_link_scrape():
	for a in a_tag:
		pdf = a.get('href')

		#Requesting Redirected URL
		redirect_url = url+pdf
		res = requests.get(redirect_url).content

		soup = BeautifulSoup(res,'lxml')

		#Scrapring All 'a' Tags
		down_button = soup.find_all('a',{"id":"download-button-link"})
		
		for down in down_button:
			download_links.append(url + down.get('href'))

pdf_download_link_scrape()
print("All Links Scraped")

#Launching Firefox
browser = webdriver.Firefox(executable_path = 'C:\\geckodriver.exe')

#Creating Folder
os.mkdir("Smartphone Hackers")

#Changing Path into Smartphone Hackers
os.chdir("Smartphone Hackers")

#Download PDF
def download_pdf():
	for download in download_links:
		
		browser.get(download)
		time.sleep(8)
		
		#Searching Hidden PDF URL	
		html = browser.execute_script("return document.documentElement.outerHTML")
		
		soup = BeautifulSoup(html,'lxml')
		pdf_file = soup.find_all('a',{"class":"btn btn-success btn-responsive"})
		
		for pdf in pdf_file:

			#Extract PDF URL
			pdf_link = pdf.get("href") 
			
			#Creating PDF Name
			name = pdf_link.split("/")[-1]
			time.sleep(10)

			#Checking Extension
			if '.pdf' in name:

				#Getting PDF Content
				pdf_response = requests.get(pdf_link).content

				#Writting PDF
				file = open(name,"wb")
				file.write(pdf_response)
				print(">>> PDF Downloded : {}".format(name))

			else:

				#Creating PDF Name
				pdf_req_url = url+name

				#Getting PDF Content
				pdf_response = requests.get(pdf_req_url).content

				#Writting PDF
				file = open(pdf_req_url+".pdf","wb")
				file.write(pdf_response)
				print(">>> PDF Downloded : {}".format(pdf_req_url))

download_pdf()
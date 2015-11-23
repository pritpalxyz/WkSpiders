import scrapy
import time
import re
from bs4 import BeautifulSoup
from WikiSpider.items import WikispiderItem

class OddsSpider(scrapy.Spider):
	name = "WikiSpider"
	allowed_domains = ["en.wikipedia.org","wikipedia.org"]
	start_urls = [		
		"https://en.wikipedia.org/wiki"	
	]

	def __init__(self):
		self.yearToSearch = input("Enter Year:")


	def parse(self,response):
		makeUrl = "https://en.wikipedia.org/wiki/%s"%(self.yearToSearch)
		makeUrl =[makeUrl]
		for url in makeUrl:
			yield scrapy.Request(url,callback=self.selectCountryPage)

	def selectCountryPage(self,response):
		countriesXpath = "//td[text()='By country']/../following-sibling::tr[1]//a/@href"
		allCountries = []
		counter = 1
		countryDict = {}
		for countryName in response.xpath(countriesXpath).extract():
			allCountries.append(countryName)
			countryDict[counter] = countryName
			counter = counter + 1
		print "***********************************"
		for data in countryDict:
			print data,":",countryDict[data]
		print "***********************************"
		selectedCountryId = input("Enter Country Id:")
		selectedUrl = countryDict[selectedCountryId]
		print "************************************"
		print "Selected Url : ",selectedUrl
		print "************************************"
		selectedUrl = "https://en.wikipedia.org%s"%(selectedUrl)
		print selectedUrl
		selectedUrl = [selectedUrl]
		for url in selectedUrl:
			yield scrapy.Request(url,callback=self.parseMainData)

	def parseMainData(self,response):
		mainHeadingXpath = 	"//h2/span[@class='mw-headline']"
		subHeadingXpath = 	"//h3/span[@class='mw-headline']/text()"
		first_file = open('WikiSpider.txt','w')
		first_file.write('url')
		first_file.write(',')
		first_file.write('information')
		first_file.write(',')
		first_file.write('additionalInfo')
		first_file.write(',')
		first_file.write('subHeading')
		first_file.write('\n')
		for mainContent in response.xpath(subHeadingXpath).extract():
			headingName = str(mainContent)
			inLoopXpath = "//h3/span[@class='mw-headline' and text()='%s']/../following-sibling::ul[1]/li"%(headingName)
			for subContent  in response.xpath(inLoopXpath).extract():
				# print subContent
				soup = BeautifulSoup(subContent)
				makeString = ""
				for textData in soup.findAll('a'):
					makeString = "%s%s"%(makeString,textData.text)
				additionalInfo =  soup.text
				first_file.write(str(response.url))
				first_file.write(',')
				first_file.write(str(makeString.encode('ascii', 'ignore')))
				first_file.write(',')
				first_file.write(str(additionalInfo.encode('ascii', 'ignore')))
				first_file.write(',')
				first_file.write(str(headingName.encode('ascii', 'ignore')))
				first_file.write('\n')
				# self.makeCsv(response.url,makeString,additionalInfo,headingName)

	
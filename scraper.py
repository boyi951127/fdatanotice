#!/usr/bin/python
# -*- coding: UTF-8 -*-
# from multiprocessing.pool import ThreadPool
import threading
from time import sleep
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import output as op
class FlaskScraper:

	# groupName: webUrl 
	dictOfNameAndWebUrl = {}

	# weburl: webCont
	dictOfNameAndWebCont = {}

	# weburl: webCOnt without mark
	dictOfNameAndWebContWithoutMk = {}

	
	# initialize
	def __init__(self, chatBot, dictOfNameAndWebsite):
		for key in dictOfNameAndWebsite:
			web = dictOfNameAndWebsite[key]
			if(key in FlaskScraper.dictOfNameAndWebUrl.keys()):
				FlaskScraper.dictOfNameAndWebUrl[key] = web
				# if(not web in FlaskScraper.dictOfNameAndWebCont.keys()):
				FlaskScraper.dictOfNameAndWebCont.setdefault(web, ['null'])
				FlaskScraper.dictOfNameAndWebContWithoutMk.setdefault(web, ['null'])		
				# FlaskScraper.dictOfNameAndWebCont.setdefault(web, self.ScraperFromFlaskByCheck(key))
			else:
				FlaskScraper.dictOfNameAndWebUrl.setdefault(key, web)
				# if(not web in FlaskScraper.dictOfNameAndWebCont.keys()):
				FlaskScraper.dictOfNameAndWebCont.setdefault(web, ['null'])	
				FlaskScraper.dictOfNameAndWebContWithoutMk.setdefault(web, ['null'])
				# FlaskScraper.dictOfNameAndWebCont.setdefault(web, self.ScraperFromFlaskByCheck(key))
				self.MultiClientController(chatBot, {key : web})
		# self.UpdateWebsiteUrl(chatBot, dictOfNameAndWebsite)
		# self.UpdateWebsiteCont(dictOfNameAndWebsite)

	def Scraper(weburl):
		driver = webdriver.Chrome("/usr/local/share/chromedriver")
		driver.get(weburl)
		try:
			driver.find_element_by_xpath("//a[contains(text(),'Show all completed tasks')]").click()
		except:
			pass

		# driver.find_element_by_id()
		# print("------------", driver.page_source)
		sleep(2)
		soup = BeautifulSoup(driver.page_source, "html.parser")
		spanlist = soup.find_all('span', attrs={'class':'best_in_place'})
		driver.quit()
		return spanlist

	# bind group name with url & bind group name with web content
	def UpdateWebsiteUrl(self, chatBot, key, web):
		# for key in incDicOfNameAndWebsite:
		# 	web = incDicOfNameAndWebsite[key]
		# print(1)
		if(web in FlaskScraper.dictOfNameAndWebUrl.values()):
			return "fail"
		# print(2)
		if(key in FlaskScraper.dictOfNameAndWebUrl.keys()):
			FlaskScraper.dictOfNameAndWebUrl[key] = web
			# if(not web in FlaskScraper.dictOfNameAndWebCont.keys()):
			FlaskScraper.dictOfNameAndWebCont.setdefault(web, ['null'])
			FlaskScraper.dictOfNameAndWebContWithoutMk.setdefault(web, ['null'])		
			# FlaskScraper.dictOfNameAndWebCont.setdefault(web, self.ScraperFromFlaskByCheck(key))
		else:
			FlaskScraper.dictOfNameAndWebUrl.setdefault(key, web)
			# if(not web in FlaskScraper.dictOfNameAndWebCont.keys()):
			FlaskScraper.dictOfNameAndWebCont.setdefault(web, ['null'])	
			FlaskScraper.dictOfNameAndWebContWithoutMk.setdefault(web, ['null'])
			# FlaskScraper.dictOfNameAndWebCont.setdefault(web, self.ScraperFromFlaskByCheck(key))
			self.MultiClientController(chatBot, {key : web})
		return "succeed"
				
				

	# multiple clients generator
	def MultiClientController(self, chatBot, nameOfGrp):
		for k in nameOfGrp:
			try:
				thread = threading.Thread(target=ScraperTimeController, args=(k, chatBot, ))
				thread.start()
			except:
				print ("Error: unable to start thread for %s !" %(k))

	# check command
	def ScraperFromFlaskByCheck(self, nameOfGrp):
		# print(dictOfNameAndWebsite.value[0])
		# html = requests.get(dictOfNameAndWebsite.values()[0]).content
		thisKey = FlaskScraper.dictOfNameAndWebUrl[nameOfGrp]
		# html = requests.get(thisKey).content
		
		# driver.get(thisKey)
		# driver.find_element_by_xpath("//a[contains(text(),'Show all completed tasks')]").click()
		# sleep(2)
		# soup = BeautifulSoup(driver.page_source, "html.parser")
		# spanlist = soup.find_all('span', attrs={'class':'best_in_place'})

		spanlist = FlaskScraper.Scraper(thisKey)

		# print("before")

		MessageWithoutMk, Message = op.ChangeFormatOfOutput(spanlist)
		# print("in")
		if (Message != FlaskScraper.dictOfNameAndWebCont[thisKey]):
			# print("in if")
			FlaskScraper.dictOfNameAndWebCont[thisKey] = Message
			# print("in if 2")
			FlaskScraper.dictOfNameAndWebContWithoutMk[thisKey] = MessageWithoutMk
			# print("in if 3")
		# print("after")

		# Message = []
		# for i in range(1,len(spanlist)):
		# 	checkbox=str(spanlist[i].find_previous_sibling('input'))
		# 	if 'checked' in checkbox:
		# 		Message.append(spanlist[i].text+'-completed')
		# 	else:
		# 		Message.append(spanlist[i].text+'-uncompleted')
		# if (Message != FlaskScraper.dictOfNameAndWebCont[thisKey]):
		# 	FlaskScraper.dictOfNameAndWebCont[thisKey] = Message	

		return Message


# time controller, send news to users
def ScraperTimeController(key, chatBot):
	while True:
		weburl = FlaskScraper.dictOfNameAndWebUrl[key]
		Message = ScraperFromFlaskByTime(weburl)
		if(Message != ['null']):
			# News=weburl + '\n' +'Update: \n'  
			News = ""
			for strMessage in Message:
				News = News + strMessage + '\n'
			News = News + weburl
			my_friend = chatBot.search(puid=key)[0]
			my_friend.send(News)
		sleep(3)


# listen to the website, return news
def ScraperFromFlaskByTime(weburl):

	spanlist = FlaskScraper.Scraper(weburl)
	print("test1")
	# driver.get(thisKey)
	# driver.find_element_by_xpath("//a[contains(text(),'Show all completed tasks')]").click()
	# sleep(2)
	# soup = BeautifulSoup(driver.page_source, "html.parser")
	# spanlist = soup.find_all('span', attrs={'class':'best_in_place'})


	# html = requests.get(weburl).content
	# soup = BeautifulSoup(html,"html.parser")
	# spanlist = soup.find_all('span',attrs={'class':'best_in_place'})

	
	MessageWithoutMk, Message = op.ChangeFormatOfOutput(spanlist)
	oldContent = []
	for v in FlaskScraper.dictOfNameAndWebContWithoutMk[weburl]:
		oldContent.append(v)
	
	# first time to log
	if (FlaskScraper.dictOfNameAndWebCont[weburl] == ['null'] and \
			Message != FlaskScraper.dictOfNameAndWebCont[weburl]):
		FlaskScraper.dictOfNameAndWebCont[weburl] = Message
		FlaskScraper.dictOfNameAndWebContWithoutMk[weburl] = MessageWithoutMk
		return Message	
	elif (Message != FlaskScraper.dictOfNameAndWebCont[weburl]):
		print(Message)
		print(MessageWithoutMk)
		print(oldContent)
		print(FlaskScraper.dictOfNameAndWebContWithoutMk[weburl])
		# print("Message",Message)
		# print("FlaskScraper.dictOfNameAndWebCont[weburl])", FlaskScraper.dictOfNameAndWebCont[weburl])
		tmplist = []
		cnt = 0
		for i in range(len(MessageWithoutMk)):
			if MessageWithoutMk[i] in oldContent:
				if Message[i] not in FlaskScraper.dictOfNameAndWebCont[weburl]:
					print("Message[%d]" %(i), Message[i])
					print("oldContent index", oldContent.index(MessageWithoutMk[i]))
					print("oldCOntent", oldContent)
					print("cont",FlaskScraper.dictOfNameAndWebCont[weburl])
					tmplist.append("\u2713 " + MessageWithoutMk[i]) # finished
				oldContent.remove(MessageWithoutMk[i])
				cnt = cnt + 1
			else:
				# print("not in MessageWithoutMk[%d]" %(i), MessageWithoutMk[i])
				# print("oldContent", oldContent)
				# print("tmplist[0]", MessageWithoutMk[i])
				print("--------------------------------")
				tmplist.append("\u2610 " + MessageWithoutMk[i])     # added
		for i in range(len(oldContent)):
			tmplist.append("\u2717 " + oldContent[i])         # delete
		
		print("final",tmplist)
		if(tmplist != []):
			FlaskScraper.dictOfNameAndWebCont[weburl] = Message
			FlaskScraper.dictOfNameAndWebContWithoutMk[weburl] = MessageWithoutMk
			return tmplist
		else:
			return ['null']
		# cnt = 0
		
	else:
		return ['null']
	# newContent = []
	# Message = []
	# oldContent = FlaskScraper.dictOfNameAndWebCont[weburl]
	# dictOldContent = {}
	# for cont in oldContent:
	# 	if cont.find('-completed') > 0:
	# 		dictOldContent[cont[:cont.find('-completed')]] ='-completed'
	# 	elif cont.find('-uncompleted') > 0:
	# 		dictOldContent[cont[:cont.find('-uncompleted')]] ='-uncompleted'
	# for i in range(1,len(spanlist)):
	# 	checkbox=str(spanlist[i].find_previous_sibling('input'))
	# 	if 'checked' in checkbox:
	# 		newContent.append(spanlist[i].text+'-completed')
	# 		if spanlist[i].text in dictOldContent.keys():
	# 			if dictOldContent[spanlist[i].text] == '-uncompleted':
	# 				Message.append('completed: '+spanlist[i].text)
	# 			dictOldContent[spanlist[i].text] = '-checked'
	# 		else:
	# 			Message.append('add: '+spanlist[i].text)
	# 	else:
	# 		newContent.append(spanlist[i].text+'-uncompleted')
	# 		if spanlist[i].text in dictOldContent.keys():
	# 			if dictOldContent[spanlist[i].text] == '-completed':
	# 				Message.append('uncompleted: '+spanlist[i].text)
	# 			dictOldContent[spanlist[i].text] = '-checked'
	# 		else:
	# 			Message.append('add: '+spanlist[i].text)
	# for cont in dictOldContent:
	# 	if dictOldContent[cont] != '-checked':
	# 		Message.append('delete: ' + cont)
	# if Message !=[]:
	# 	FlaskScraper.dictOfNameAndWebCont[weburl]=newContent
	# 	return Message
	# else:
	# 	return ['null']




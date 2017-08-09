# http://wxpy.readthedocs.io/
# https://github.com/youfou/wxpy

from wxpy import *
import scraper
import pickle
# aye=XiaoI('C1T75cDNfqqT','Afm5HFFirhqjE07KhD23')
# aye=Tuling(api_key='df15a092f37c4032aef5be2b6356caa5')

bot=Bot(cache_path=True)
bot.enable_puid()

# clear initializd website
global website
f=open('website.pkl','wb')
website={}
pickle.dump(website,f)
f.close()

# read initial website
with open('website.pkl','rb') as f:
	website=pickle.load(f)
print("initial website:", website)

global flaskScraper
flaskScraper = scraper.FlaskScraper(bot, website)
listWeb = []
for key in website.keys():
	listWeb.append(key)


@bot.register()
def print_messages(msg):
	if msg.text == 'check':
		print(1)
		msg_puid = msg.chat.puid
		if not msg_puid in website.keys():
			return 'please register before check!'
		print(2)
		todo_list = flaskScraper.ScraperFromFlaskByCheck(msg_puid)
		# message = website[msg_puid] + '\n' +'List: \n'
		message = ""
		for i in range(len(todo_list)):
			message = message + todo_list[i] + '\n'
		print(3)
		print(website[msg_puid])
		print(4)
		message = message + website[msg_puid]
		print(5)
		return message

	elif 'https://flask.io/' in msg.text :
		msg_website = msg.text
		if ' ' in msg_website:
			return 'please just send the website address~'
		
		msg_puid = msg.chat.puid
		website[msg_puid] = msg_website

		try:
			state = flaskScraper.UpdateWebsiteUrl(bot, msg_puid, msg_website)
		except:
			return 'Invalid URL'
		else:
			if(state == "succeed"):
				return 'get your to-do list successfully!'
			elif(state == "fail"):
				return 'the address has been registered already!'
		
	# else:
		# aye.do_reply(msg)
		

# 堵塞线程，并进入 Python 命令行
# embed()
bot.join()

with open('website.pkl','wb') as f:
	pickle.dump(website,f)
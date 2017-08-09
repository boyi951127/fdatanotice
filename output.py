import scraper

def ChangeFormatOfOutput(spanlist):
	# str = str+"u\u2713"
	# str = str+"u\u2610"
	# return str
	Message = []
	MessageWithoutMk = []
	# print("in")
	for i in range(1, len(spanlist)):
		# print("span", spanlist[i].text)
		checkbox = str(spanlist[i].find_previous_sibling('input'))
		if 'checked' in checkbox:
			Message.append("\u2713 " + spanlist[i].text)
			MessageWithoutMk.append(spanlist[i].text)
		else:
			Message.append("\u2610 " + spanlist[i].text)
			MessageWithoutMk.append(spanlist[i].text)
	# print(Message)
	
	return MessageWithoutMk, Message
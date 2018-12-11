import re
import sqlite3
import language_check

#import time
from datetime import datetime

import HTMLParser

from textblob import TextBlob
from textstat.textstat import textstat

from bs4 import BeautifulSoup


def getBodysCount(text):
##return a tuple with body words count and body politeness
	
	whWordList = r'\b(what|why|when|who|which|how|whose|whom)\b';
	politessList = r'\b(thank|thanks|please|could|would|help)\b';

	whc = 0; 	#wh words count
	pc = 0 		#politeness count
	corpus = text;
	splitao = corpus.split(" ")
	for  t in splitao:
		termo = t.lower();

		if(re.search(whWordList, termo)):
			whc = whc + 1;
		if(re.search(politessList, termo)):
			pc = pc + 1
	
	return (whc, pc);

def getWordsCount(text): 

##
	
	pattern = r'\b.*[a-z]+.*\b';
	c = 0;
	corpus = text;
	splitao = corpus.split(" ")
	for  t in splitao:
		termo = t.lower();

		if(re.search(pattern, termo)):
			c = c + 1;
	
	return c;


###beginning execution
ticks = datetime.now()
#print("process beginning :::" + time.asctime(time.localtime(ticks) ))
print("process beginning :::" + ticks.strftime("%Y-%m-%d %H:%M:%S"))

html_parser = HTMLParser.HTMLParser()



# lendo os dados

tableName = "SampleLINEARALGEBRA"

#get bodyNoCode

selectQuery = " SELECT  body, id FROM " + tableName + " where id >= 0 order by id LIMIT 100000 "

conn = sqlite3.connect("C:\Software\sqlite\cqadb.db")

cursor = conn.cursor()

cursor.execute(selectQuery)

tool = language_check.LanguageTool('en-US')

i = 0

all_rows = cursor.fetchall()

total_rows = len(all_rows)

for linha in all_rows:
	
 	print("\nid :: %s [%d of %d ]" % (linha[1],i, total_rows  ) 	)
	id_question = linha[1]

 	texto = linha[0]

	soup = BeautifulSoup(texto, 'html.parser')
 	#print("\nbody html\n")
 	#print(soup.prettify())
 	

 	#get body no html
 	#print("\nbody text\n")
 	soup_nohtml = soup.get_text()
 	#print(soup_nohtml)


 	#get body no code

 	#soup_nocode = soup.code.decompose()
 	
 	for code in soup("code"):
		code.decompose()

 	soup_nocode = soup.get_text()
 	#print("\nbody no code\n")
 	#print(soup_nocode) 	

 	#get question (body) no html word count
 	bodyWordCount = getWordsCount(soup_nohtml)

 	#get question (body) length
 	bodyLength = len(soup_nohtml)

 	#get question (body) no html wh word count
 	body_counts = getBodysCount(soup_nocode)
 	
 	bodyWhCount = body_counts[0]

 	#get question (body) politeness
 	bodyPoliteness = body_counts[1]

 	#calculate language error
 	if len(soup_nocode) > 0:
 		matches = tool.check(soup_nocode)
 	else:
 		matches = []
	
	"""
 	if matches :
 		for m in matches:
 			
 			print(" Error found: \n")
 			try:
 				print(m)
 			except:
 				print( " texto has some character not available for print ::: ")
			"""
 	#calculate subjectivity

	testimonial = TextBlob(soup_nocode)

	polarity_val = testimonial.sentiment.polarity
	subjectivity_val = testimonial.sentiment.subjectivity
	#print("\nAverage sentiment::\n")
	#print(testimonial.sentiment)
	# for t in testimonial.sentences:
	# 	print("\nsentiment :::\n ") 
	# 	print(t)
	# 	print(t.sentiment)

	

 	#calculate readability
 	#print("\nAverage readability::\n")
 	if(len(soup_nohtml) > 1):
		readability_val =  textstat.text_standard(soup_nohtml)
		readability_score = readability_val.split("th")[0]
	else:
		readability_score = 0

	#get the number of the lower grade
	

	#print(readability_val)
	#print(readability_score)

 	# update values

 	# alterando os dados da tabela
 	
	cursor.execute("""
	UPDATE """ + tableName + """
	SET LanguageErrors = ?, Polarity = ?, Subjectivity = ?, Readability = ?, whBodyCount = ?, bodynocode = ?, bodynohtml = ?, bodywordcount = ?, QuestionLength = ?, bodyPoliteness = ?
	WHERE id = ?
	""", (len(matches), polarity_val, subjectivity_val, readability_score, bodyWhCount, soup_nocode, soup_nohtml , bodyWordCount, bodyLength, bodyPoliteness, id_question))

	conn.commit()

	i = i + 1
	
	#print( ( " Number of language errors: %s") % (len(matches) if matches else 0))

conn.close()

###ending execution
ticks_end = datetime.now()
#print("process ending :::" + time.asctime(time.localtime(ticks_end) ))
print("process ending :::" + ticks_end.strftime("%Y-%m-%d %H:%M:%S") )

delta = ticks_end - ticks
print("execution time:: %d seconds" % delta.total_seconds() )
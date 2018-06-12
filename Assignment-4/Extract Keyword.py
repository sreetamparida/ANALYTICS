# IMPORTED REQUIRED PACKAGES 
import pandas as pd
import nltk
#nltk.download('book')
import string
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
import PyPDF2

#Read the PDF file using PyPDF2
file = 'JavaBasics-notes.pdf'
pdf = open(file,'rb')
read_pdf = PyPDF2.PdfFileReader(pdf)

#Retrieve the page number to extract text from pages
pages = read_pdf.numPages
count = 0
text = ''

#Extraction of text from the pages of the pdf file
while count < pages:
    page = read_pdf.getPage(count)
    count +=1
    text += page.extractText()

#Text preprocessing to extract sentences out of text
text = text.lower()
#Replaced '!' with '.' as PyPDF2 reads bullets as !
'''
For eg:
    1.TextA
    2.TextB

will be read as 
    !TextA!TextB
    by PyPDF2
hence replacing '!' with '.' treats them as separate sentences
'''
text = text.replace('!','.')

#Extraction of sentences from text
sentence = text.split('.')
for sen in sentence:
    if len(sen.split())==0 or len(sen.split())==1:
        sentence.remove(sen)


#Creation of DataFrame of the extracted sentences
df = pd.DataFrame(sentence,columns=['Text'])

#Function to process the text
'''
    1.remove digits
    2.remove punctuations
    3.remove stopwords
    4.check if word in dictionary
    5.return keywords

'''
def text_processor(x):
    no_digit = [letter for letter in x if not letter.isdigit()]
    no_digit = ''.join(no_digit)
    no_punc = [char for char in no_digit if char not in string.punctuation]
    no_punc = ''.join(no_punc)
    token = [word for word in no_punc.split() if word not in stopwords.words('english')]
    keyword = [key for key in token if wordnet.synsets(key)]
    return keyword

#Implemented text_processor() as analyser in CountVectorizer and fitting was done over the extracted sentences
bow = CountVectorizer(analyzer=text_processor).fit(df['Text'])
text_bow = bow.transform(df['Text'])

#Tfidf was used to find their importance or weight over the PDF
tfidf = TfidfTransformer().fit(text_bow)
tfidf_tranform = tfidf.transform(text_bow)

#Assignment of weights to keywords
key_weight = {}
for i,word in enumerate(bow.get_feature_names()):
    if len(word)!=1:
        weight = tfidf_tranform.getcol(i).mean()
        key_weight[word]=weight*10

#Creation of DataFrame and exported as "key_weight.xlsx"
df_weight = pd.DataFrame.from_dict(key_weight,orient='index')
df_weight.to_excel('key_weight.xlsx')


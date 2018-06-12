
import pandas as pd
import numpy as np

#READ the csv
df = pd.read_csv('Automatic email content store.csv',sep='$')

#Extraction of Unique Mail
unique_mail = list(df['to '].unique())

#Function to get rows with proper date format

def get_rows(x):
    c = len(x.split('/'))
    
    if c!= 3:
        ind = df[df['Date']==x].index
        df.drop(ind,inplace=True)
        return 'deleted'
    else:
        return 'in_format'

#Application of that function to remove rows not in proper format
df['Date'].apply(get_rows)
df.reset_index(inplace=True)

# ### 22nd index has been deleted as it did not have date in required format

#Retrieved last index and last date 
last_index = len(df)-1
last_date = df.loc[last_index]['Date']


# # Function to get  number of days number of days between the last date and given date

def get_days(x):
    last_date = df.loc[last_index]['Date']
    last_date = pd.to_datetime(last_date,dayfirst=True)
    to_date = pd.to_datetime(x,dayfirst=True)
    no_days = np.absolute((last_date-to_date).days)
    return no_days

get_days('17/10/17')


# # Checking if the words present in array are in content
# As no matching words were there, a dummy array has been created
lang_array = ['Python','C','C++','OpenCV','Jave']
dummy_array = ['can','you','doing']

def get_word(x):
    ls = [word.lower() for word in x.split()]
    ls = set(ls)
    
    #here you can replace for arrray having OpenCV, Python 
    # As no matching words were there, a dummy array has been created
    arr = set(dummy_array)
    result = ';'.join(list(arr.intersection(ls)))
    if len(result)==0:
        return 'Nothing Matched'
    else:
        return result

#Application of function to extract word
df['array_cont'] = df['raw'].apply(get_word)

df.to_excel('Mail_analysis.xlsx')


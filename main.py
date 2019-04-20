
from time import sleep
import pandas as pd
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl

df = pd.read_excel('IG.xlsx',usecols=0)
#print(df.columns)
fname_list = list(df.iloc[:,0])
fname_list = list(map(str.strip, fname_list))

f_list = list()
# print(fname_list)
count = 0 
error = []
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
print("------------------Starting Retrival------------------")
for i in range(len(fname_list)):
    try:
        baseUrl = "https://www.instagram.com/" + fname_list[i].strip()
        html = urllib.request.urlopen(baseUrl).read()
        count+=1
        soup = BeautifulSoup(html,'html.parser')
        for link in soup.find_all('meta',property='og:description'):
            a = link.get('content')
        a = a.split(" ")
        if(a[1] == 'Followers,'):
            follower = a[0]
            f_list.append(a[0])
        print(f"User Name : {fname_list[i]} \t No. of follower = {follower}")
        if(count%10 == 0):
            print('\n\nDo no close the window \n\n')
            sleep(5)
    except:
        print("User Name :",fname_list[i].strip(),"Not found")
        f_list.append('Wrong Username')
        error.append(fname_list[i].strip())
        continue

print(f"\n\t\tFollower Retrival Done..\n\nTotal Username in Excel Sheet : {len(fname_list)}\nTotal Username's Followers Retrived : {count}\n\n\t")
if(len(error) != 0):
    print("Username's not retrived due to error :")
    [print(f'\t{i}') for i in error]
print('\n\n\nSaving data to IG_Retrived.xlsx...')
#for i in
q_list = list()
for i in f_list:
    if(i[-1] == 'm'):
        a = float(i[:-1]) * 1000000
        q_list.append(a)
    elif(i[-1] == 'k'):
        a = float(i[:-1]) * 1000
        q_list.append(a)
    else:
        q_list.append(i)
df['Count'] = q_list
df.to_excel("IG_Retrived.xlsx")
sleep(5)
print("Data Saved.\nPress enter key to exit...")
sleep(2)
n = input()
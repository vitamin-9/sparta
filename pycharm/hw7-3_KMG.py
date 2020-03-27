import requests
from bs4 import BeautifulSoup

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20200309',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

music_info = soup.select('#body-content > div.newest-list > div > table.list-wrap>tbody>tr')
rank = 0
for music in music_info:
    rank +=1
    title_tmp = music.select('td.info > a.title.ellipsis')
    singer_tmp = music.select('td.info > a.artist')
    title_tmp2 = title_tmp[0].text
    title = title_tmp2.strip()
    singer = singer_tmp[0].text
    print (rank, title, ',', singer)
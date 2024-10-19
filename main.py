import sys
from bs4 import BeautifulSoup
import requests

sys.stdout.reconfigure(encoding='utf-8')
try:
    # Fetch the webpage content
    response = requests.get("http://127.0.0.1:5500/index.html")
    soup = BeautifulSoup(response.text, 'html.parser')
    movies = soup.find('tbody').find_all('tr')

    for movie in movies:
        #print(movie)
        movie_name = movie.find('td').text
        rating = movie.find('td', class_="rating").text
        year = movie.find('td', class_="year").text
        duration = movie.find('td', class_="duration").text
        print("🎥",movie_name, "⭐", rating,  "🗓", year, "🕦",duration)
        

    # Print out the content while ensuring special characters are handled correctly
    #print(soup.prettify().encode('utf-8', 'ignore').decode('utf-8'))
except Exception as e:
    print(e)

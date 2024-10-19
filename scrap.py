from bs4 import BeautifulSoup
import requests, sys, openpyxl

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

excel = openpyxl.Workbook()
sheet = excel.active
sheet.title = "Movie List"
sheet.append(["Rank", "Movie Name", "Year of Release", "IMDB Rating", "Movie Duration"])

sys.stdout.reconfigure(encoding = "utf-8")

try:
    response = requests.get("https://www.imdb.com/chart/top/", headers=headers)
    
    soup = BeautifulSoup(response.text, 'html.parser')

    movies = soup.find('ul', class_="ipc-metadata-list")

    for movie in movies.find_all('li', class_='ipc-metadata-list-summary-item'):

        movie_name = movie.find('h3', class_='ipc-title__text').text.split('.')[1]

        movie_rank = movie.find('h3', class_="ipc-title__text").text.split('.')[0]
        movie_year = movie.find('span', class_='sc-732ea2d-6 gbTbSy cli-title-metadata-item').text.strip()
    
        # Get duration
        movie_duration = movie.find_all('span', class_='sc-732ea2d-6 gbTbSy cli-title-metadata-item')[1].text.strip()
    
        # Get rating
        movie_rating = movie.find('span', class_='ipc-rating-star--rating').text.strip()

        #print(movie_rank, "🎥",movie_name, "⭐", movie_rating,  "🗓", movie_year, "🕦",movie_duration)

        sheet.append([movie_rank, movie_name, movie_year, movie_rating, movie_duration])

except Exception as e:
    print(e)


excel.save("Movie.xls")
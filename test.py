import sys, openpyxl, requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

excel = openpyxl.Workbook()
sheet = excel.active
sheet.title = "Movie List"
sheet.append(["Rank", "Movie Name", "Movie Year", "Movie Rating", "Duration", "Meta Score", "Description"])
sys.stdout.reconfigure(encoding="utf-8")

try:
    response = requests.get("https://www.imdb.com/search/title/?title_type=feature&num_votes=25000,&genres=adventure&sort=user_rating,desc", headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    movies = soup.find('ul', class_="sc-748571c8-0")
    for movie in movies.find_all('li', class_="ipc-metadata-list-summary-item"):
        movie_rank = movie.find('h3', class_="ipc-title__text").text.split('.')[0]
        movie_name = movie.find('h3', class_="ipc-title__text").text.split('.')[1]
        movie_year = movie.find('span', class_="sc-732ea2d-6").text
        movie_duration = movie.find_all('span', class_="sc-732ea2d-6")[1].text.strip()
        movie_rating = movie.find('span', class_="ipc-rating-star--rating").text
        try:
            movie_meta_score = movie.find('span', class_="sc-b0901df4-0").text.strip()
        except Exception as e:
            print()
        movie_description = movie.find('div', class_="ipc-html-content-inner-div").text
        #sheet.append(["Rank", "Movie Name", "Movie Year", "Movie Rating", "Duration" "Meta Score"])

        sheet.append([movie_rank, movie_name, movie_year, movie_rating, movie_duration, movie_meta_score, movie_description])
        #print(movie_rank, movie_name, movie_year, movie_duration, movie_rating, movie_meta_score)
        # print(movie_description, "\n")
except Exception as e:
    print(e)
    
excel.save("Movie_List2.xls")
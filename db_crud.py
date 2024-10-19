import sys, requests, sqlite3 , pandas as pd
from bs4 import BeautifulSoup

#Using Headers for Mimic like a Original Browser to avoid blocked by the associate website
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

#Use Utf-8 Encoding to suppport all type of Unicode Characters
sys.stdout.reconfigure(encoding="utf-8")

try:
    response = requests.get("https://www.imdb.com/search/title/?title_type=feature&num_votes=25000,&genres=adventure&sort=user_rating,desc", headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    movies = soup.find('ul', class_="sc-748571c8-0")
    movies_list={
        "movie_rank": [],
        "movie_name": [],
        "movie_year": [],
        "movie_duration": [],
        "movie_description":[],
        "movie_metascore":[],
    }
    for movie in movies.find_all('li', class_="ipc-metadata-list-summary-item"):
        movie_rank        = movie.find('h3', class_="ipc-title__text").text.split('.')[0]
        movie_name        = movie.find('h3', class_="ipc-title__text").text.split('.')[1]
        movie_year        = movie.find('span', class_="sc-732ea2d-6").text
        movie_duration    = movie.find_all('span', class_="sc-732ea2d-6")[1].text.strip()
        movie_rating      = movie.find('span', class_="ipc-rating-star--rating").text
        movie_description = movie.find('div', class_="ipc-html-content-inner-div").text

        #Use Error handling for a Particular content becoz Some Data have this particular content
        #So Avoiding Data loss after this Empty data using Exception Handling
        try:
            movie_meta_score = movie.find('span', class_="sc-b0901df4-0").text.strip()
        except Exception as e:
            print()
            
        #Appending all the Scraped Data to the List in Dictionary(movie_list)
        movies_list["movie_rank"].append(movie_rank)
        movies_list["movie_name"].append(movie_name)
        movies_list["movie_year"].append(movie_year)
        movies_list["movie_duration"].append(movie_duration)
        movies_list["movie_description"].append(movie_description)
        movies_list["movie_metascore"].append(movie_meta_score)
        
except Exception as e:
    print(e)
    
    
#Converting the Dictionary Data to Data Frames using pandas
df = pd.DataFrame(movies_list)
print(df.head())
#Create a DB & DBConnection 
connection = sqlite3.connect("test.db")

#Create a cursor Object for DB Manipulation(Process)
cursor = connection.cursor()

#SQL Query for Creating the table 
qry = "CREATE TABLE IF NOT EXISTS movies(movie_rank, movie_name, movie_year, movie_duration, movie_description, movie_meta_score)"  

#Create table movies using the qry  
cursor.execute(qry)

#Fetch the Data uing iloc method in pandas by slicing
for i in range(len(df)):
    cursor.execute("insert into movies values (?,?,?,?,?,?)", df.iloc[i])
    
connection.commit()
connection.close()
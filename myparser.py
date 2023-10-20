import requests
from bs4 import BeautifulSoup

urlMain = 'https://litmir.club'
urlAllGenre = 'https://litmir.club/all_genre'


# Получить словарь жанров {ключ: название жанра, значение: словарь поджанров}.
# Словарь поджанров {ключ: название поджанра, значение: ссылка на поджанр}.
def get_dictionary_genres():
    response = requests.get(urlAllGenre)
    soup = BeautifulSoup(response.text, 'lxml')

    dictionaryGenres = dict()
    islands = soup.find_all('div', class_='island')[1:]

    for island in islands:
        nameGenre = island.find('p', class_='genre_title').text

        dictionarySubGenres = dict()
        hyperlinks = island.find_all('a', class_='lt29')

        for hyperlink in hyperlinks:
            nameSubGenre = hyperlink.find('span', class_='underline genre_item').text
            ref = urlMain + hyperlink['href']

            dictionarySubGenres[nameSubGenre] = ref

        dictionaryGenres[nameGenre] = dictionarySubGenres

    return dictionaryGenres


# Получить словарь книг (трёх книг) {ключ: название книги, значение словарь книги}.
# Словарь книги {ключ: атрибут, значение: значение атрибута}.
# Список атрибутов: ссылка на книгу, оценка, описание, авторы.
def get_dictionary_books(dictionaryGenres, nameGenre, nameSubGenre):
    ref = dictionaryGenres[nameGenre][nameSubGenre]

    response = requests.get(ref)
    soup = BeautifulSoup(response.text, 'lxml')

    dictionaryBooks = dict()
    islands = soup.find_all('table', class_='island')[:3]

    for island in islands:
        divNameBook = island.find('div', class_='book_name')
        nameBook = divNameBook.text.strip()

        dictionaryBook = dict()

        ref = divNameBook.find('a')['href']
        dictionaryBook['ref'] = urlMain + ref.strip()

        spanGrade = island.find('span', class_='orange_desc')
        grade = 'Отсутствует' if spanGrade is None else spanGrade.text
        dictionaryBook['grade'] = grade.strip()

        divDescBox = island.find('div', class_='desc_box')
        authors = [x.text.strip() for x in divDescBox.find_all('a') if x.text != '...']
        dictionaryBook['authors'] = authors

        description = island.find('div', class_='lt37').text
        if 'Полное описание' in description:
            description = description.replace('Полное описание', '')
        dictionaryBook['description'] = description.strip()

        dictionaryBooks[nameBook] = dictionaryBook

    return dictionaryBooks

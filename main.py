import ssl

import requests
import urllib3.exceptions
from bs4 import BeautifulSoup
import pdfrw
from datetime import date

search_keywords = ["inec", "bvas", "pdp", "apc", "adc", "buhari","obi"]

try:
    # Set the user agent to a common web browser
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

    # Request the webpage (using session to accept cookies, so we can bypass bot checks)
    url = "https://punchng.com/topics/news/"
    session = requests.Session()

    # Request the website to get the cookies
    response = session.get(url, headers=headers)

    # Extract the cookies from the response
    cookies = response.cookies

    # Use the cookies in the next request
    response = session.get(url, headers=headers, cookies=cookies)

    soup = BeautifulSoup(response.text, "html.parser")
    # print(soup.text)

    # Find all the articles on the webpage
    articles = soup.find_all("h1", class_="post-title")

    # Create an empty list to store the relevant articles
    relevant_articles = []

    # Check if each article contains the keyword
    for article in articles:
        for search_keyword in search_keywords:
            if search_keyword.lower() in article.text.lower():
                relevant_articles.append({"title": article.text, "url": article.findNext("a").attrs.get("href"), "keyword": search_keyword})
                # print(article)
                # print(article.findNext("a").attrs.get("href"))

    # Create the PDF
    pdf = pdfrw.PdfWriter()

    # Add the relevant articles to the PDF
    for article in relevant_articles:
        # pdf.addpage(pdfrw.Page(article))
        pass

    # Save the PDF with today's date as the file name
    filename = "election_articles_" + str(date.today()) + ".pdf"
    pdf.write(filename)

    # print(len(relevant_articles))
    print(relevant_articles)
except requests.exceptions.RequestException as e:
    # Handle network errors
    print("An error occurred:", e)
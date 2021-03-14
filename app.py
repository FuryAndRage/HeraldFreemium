
from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
app = Flask(__name__)

def get_news(url):
	if 'https' in url:
		url.replace('https','http')
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	h1 = soup.find('a', class_='article-bigread__heading__link')
	h1_text = ''
	try:
		h1_text = h1.text
	except Exception as e:
		h1_text = h1
		
	article = soup.find('section', class_='article__body')
	tag_p = article.find_all('p')
	
	new_p = (item.get_text() for item in tag_p)
	context = {'p':new_p, 'h1':h1_text}
	
	
	return context

@app.route('/', methods=['POST','GET'])
def main():
	if request.method == 'POST':
		url = request.form.get('url')
		res = get_news(url)
		
		return render_template('crawler.html', res = res)
	else:
		return render_template('crawler.html')
if __name__ == '__main__':
	app.run(host= '0.0.0.0',debug=True)


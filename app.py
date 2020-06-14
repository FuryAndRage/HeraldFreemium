
from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
app = Flask(__name__)

def get_news(url):
	if 'https' in url:
		url.replace('https','http')
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	h1 = soup.find('h1')
	img = soup.find_all('figure')
	article = soup.find(id = 'article-content')
	p_article = article.find_all('p')
	new_p = (item.get_text() for item in p_article)

	img = soup.find_all('figure')
	img_url = ''
	try:
		img_url = [i.find('img')['src'] for i in img]
		print(img_url)
		if not img_url:
			img_url = [i.find('video') for i in img]
			print(img_url, 'esse resultado')
	except:
		print('nada')
	context = {'p':new_p, 
	'h1':h1.text,
	'img':img_url[0]}
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
	app.run(host= '0.0.0.0')


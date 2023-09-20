from flask import Flask, render_template, request
from ytlib import getTrendingVideos, getSearchResults, grabVideoLink

app = Flask(__name__)

@app.route('/')
def trending():
    videos = getTrendingVideos()
    return render_template('trending.html', videos=videos)

@app.route('/watch/<id>')
def watch(id):
    videoLink = grabVideoLink(id)
    return render_template('watch.html', videoLink=videoLink)

@app.route('/search')
def search():
    query = request.args.get('query')
    searchResults = getSearchResults(query)
    return render_template('search.html', query=query, results=searchResults)

if __name__ == '__main__':
    app.run(debug=True)
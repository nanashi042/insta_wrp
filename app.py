import time
from flask import Flask, render_template
from flask_caching import Cache
from apscheduler.schedulers.background import BackgroundScheduler
from utils.wallpaper import Wallpaper

app = Flask(__name__)

# Configure Flask-Caching
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Configure Flask-APScheduler
scheduler = BackgroundScheduler()
scheduler.start()

# Set a flag to control whether to manually refresh the cache
manual_refresh = False

@app.route('/')
@cache.cached(timeout=5, key_prefix='img_links')  # Cache the result for 24 hours
def hello_world():
    global manual_refresh
    if manual_refresh:
        # Manually refresh the cache
        update_cache()
        manual_refresh = False
    links = ''.join(get_img())
    print(str(links))
    return render_template('index.html', links=links)

def get_img():
    obj = Wallpaper()
    links = obj.extract_links()
    yield links

# Schedule the job to refresh the cache every 24 hours
@scheduler.scheduled_job('interval', seconds=5)
def update_cache():
    cache.clear()
    print("Cache cleared.")

# Manually trigger cache refresh by setting manual_refresh to True
@app.route('/manual_refresh')
def manual_cache_refresh():
    global manual_refresh
    manual_refresh = True
    return 'Cache will be refreshed manually.'

if __name__ == "__main__":
    app.run(debug=True)

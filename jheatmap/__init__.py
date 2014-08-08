VERSION = "0.2.0"
AUTHORS = "Michael P Schroeder"
CONTACT_EMAIL = "michael.p.schroeder@gmail.com"

from jheatmap.widget_jheatmap import JHeatmap

def _publish_js():

    from IPython.display import display, Javascript
    with open('jheatmap/widget_jheatmap_loader.js', 'r') as f:
        display(Javascript(data=f.read()))

## publish javascript to ipython notebook html
_publish_js()

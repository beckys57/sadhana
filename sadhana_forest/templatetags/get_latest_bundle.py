from django import template
from sadhana_forest.settings import ASSETS_DIR

import os 

register = template.Library()

@register.simple_tag
def bundle_filename():
    
    filename = [file for file in [f for f in os.walk(ASSETS_DIR+'build/static/js/')][0][2] if file[-3:] == '.js'][0]
    return filename
import os
import re

import jinja2

TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
env = jinja2.Environment(autoescape=False, loader=jinja2.FileSystemLoader(TEMPLATE_DIR))
template = env.get_template('docs/github/README.template')
output = template.render()


with open('../../README.rst', 'w') as f:
    f.write(output)

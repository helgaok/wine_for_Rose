from http.server import HTTPServer, SimpleHTTPRequestHandler
import datetime, pandas, pprint
from collections import defaultdict

from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

now_year = datetime.datetime.now()

excel_data_df = pandas.read_excel('wine.xlsx')
excel_data_wine2 = pandas.read_excel('wine2.xlsx', na_values=['N/A', 'NA'], keep_default_na=False)
excel_data_wine3 = pandas.read_excel('wine3.xlsx', na_values=['N/A', 'NA'], keep_default_na=False)

excel_dict = excel_data_df.to_dict(orient='records')
excel_list_wine2 = list(excel_data_wine2.to_dict('records'))
excel_list_wine3 = list(excel_data_wine3.to_dict('records'))

wines_dict = defaultdict(list)

for wine in excel_list_wine3:
  wines_dict[wine['Категория']].append(wine)

print(pprint.pprint(wines_dict))

rendered_page = template.render(
    age_of_winery=now_year.year - 1920,
    wines_dict = wines_dict
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
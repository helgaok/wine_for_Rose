import datetime
from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape


def main():
  env = Environment(
      loader=FileSystemLoader('.'),
      autoescape=select_autoescape(['html', 'xml'])
  )

  template = env.get_template('template.html')

  excel_wine3 = pandas.read_excel('wine3.xlsx', na_values=['N/A',       'NA'], keep_default_na=False)

  wines_from_excel = list(excel_wine3.to_dict('records'))

  grouped_wines = defaultdict(list)

  for product in wines_from_excel:
    grouped_wines[product['Категория']].append(product)

  winery_foundation_date = 1920

  rendered_page = template.render(
      age_of_winery=datetime.datetime.now().year -       winery_foundation_date,
      grouped_wines = grouped_wines
  )

  with open('index.html', 'w', encoding="utf8") as file:
      file.write(rendered_page)

  server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
  server.serve_forever()
  
if __name__ == '__main__':
  main()
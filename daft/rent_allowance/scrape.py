import requests
from bs4 import BeautifulSoup

def scrape_table(url, table_id):
    """
    Convert a table with `table_id` at `url` into list of dicts.
    """
    #url = "http://www.citizensinformation.ie/en/social_welfare/social_welfare_payments/supplementary_welfare_schemes/rent_supplement.html#l62fd2"
    req = requests.get(url)
    content = req.content
    soup = BeautifulSoup(content)

    table = soup.find('table', table_id)

    first_row = table.tr

    header_cells = table.tr.findAll('td')

    headings = map(lambda x: clean_string(x.text), header_cells)

    json_data = []
    rows = table.findAll('tr')

    # loop through rows, skipping the header row
    for row in rows[1:]:
        cells = row.findAll('td')
        values = map(lambda x: x.text, cells)
        key_value = dict(zip(headings, values))
        json_data.append(key_value)

    return json_data

def clean_string(title):
    return " ".join(title.split())

import pandas as pd
import numpy as np
import requests
import bs4

def allowed_by_robots_txt(url):
    """
    Returns a boolean value representing if a url is allowed 
    to be scraped, according to the site's robots.txt
    ---
    url: string representing url to scrape
    """
    # Get robots.txt
    url_split = url.split("/")
    robots_txt_url = url_split[0] + '//' + url_split[2] + '/robots.txt'

    response = requests.get(robots_txt_url)
    response.raise_for_status()

    lines = response.text.split('\n')

    user_agent_allowed = True

    for line in lines:
        if line.lower().startswith('disallow'):
            # Check if the URL is disallowed
            disallowed_path = line.split(':', 1)[1].strip()
            if url.endswith(disallowed_path):
                return False

    # If no specific rule is found, the URL is allowed
    return True

def get_pokedex(url):
    """
    Returns a DataFrame object that contains the Pokédex for the url to the specified generation.
    ---
    url: string representing url to scrape
    """
    # Make request to site
    response = requests.get(url)
    
    # Check to see if response was successful
    if response.status_code == 200:
        html_content = response.text
    else:
        raise Exception(f"Error: Unable to fetch content. Status code: {response.status_code}.")
        
    # create soup object and get only 'tr' tags
    soup = bs4.BeautifulSoup(html_content, features='lxml')
    soup = soup.find('div', class_='resp-scroll').find_all('tr')
    
    # get column data
    column_info = soup[0]
    column_info = column_info.find_all('th')
    
    # get data
    num, name, elements, total, hp, attack, defense, spatk, spdef, spd = [], [], [], [], [], [], [], [], [], []
    for pokemon in soup[1:]:
        num.append(pokemon.find_all('td')[0].text)
        name.append(pokemon.find_all('td')[1].text)
        elements.append(pokemon.find_all('td')[2].text)
        total.append(pokemon.find_all('td')[3].text)
        hp.append(pokemon.find_all('td')[4].text)
        attack.append(pokemon.find_all('td')[5].text)
        defense.append(pokemon.find_all('td')[6].text)
        spatk.append(pokemon.find_all('td')[7].text)
        spdef.append(pokemon.find_all('td')[8].text)
        spd.append(pokemon.find_all('td')[9].text)
    
    # combine column data and raw data to form DataFrame
    data = {column_info[0].text: num, 
            column_info[1].text: name, 
            column_info[2].text: elements, 
            column_info[3].text: total, 
            column_info[4].text: hp, 
            column_info[5].text: attack, 
            column_info[6].text: defense, 
            column_info[7].text: spatk, 
            column_info[8].text: spdef, 
            column_info[9].text: spd}
    return pd.DataFrame(data)
import requests
import bs4
from bs4 import BeautifulSoup, NavigableString, Tag


# function to get URLs from page
def get_url_title(url):
  page = requests.get(URL)
  soup = BeautifulSoup(page.text, 'html.parser')
  #finds all links to API/API Standards as listed on the page
  links = [a['href'] for a in soup.find_all('a', href=True)]
  filtereddivs = list(filter(lambda x: '/developer/api-catalogue/' in x, links))
  beg = 'https://digital.nhs.uk'
  urls = []
  for link in filtereddivs:
    # removes standards links based on 'standard' being in url
    if 'standard' in link:
      continue
    else:
      url = beg + link
      urls.append(url)
  return urls


# function to pull out all information between h2 headers
def get_api_info(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    headers_text_dict = {}
    for header in soup.find_all('h2'):
        contain = ''
        nextNode = header
        while True:
            nextNode = nextNode.nextSibling
            if nextNode is None:
                if 'overview' in header.text.lower():
                    svgs = soup.find_all('svg')
                    for svg in svgs:
                        if svg.find_next_sibling('div', 'nhsd-!t-margin-bottom-6') is not None:
                            contain = contain + ' ' + svg.find_next_sibling('div', 'nhsd-!t-margin-bottom-6').get_text(
                                strip=True).strip()
                break
            if isinstance(nextNode, NavigableString):
                pass
            if isinstance(nextNode, Tag):
                if nextNode.name == "h2":
                    break
                contain = contain + ' ' + nextNode.get_text(strip=True).strip()
        headers_text_dict[header.text.strip().lower()] = contain

    return headers_text_dict


# pulls out the overview from the dictionary from the api-info function and creates a list of dictionaries
def create_filtered_dict(apis, megadict):
    new_dict = {}
    page = requests.get(apis)
    soup = BeautifulSoup(page.text, 'html.parser')
    title = soup.find(class_='nhsd-t-heading-xxl nhsd-!t-margin-bottom-0').text
    name = title
    description = megadict['overview']
    url = apis
    new_dict['name'] = name
    new_dict['description'] = description
    new_dict['url'] = url
    new_dict['contact'] = 'https://digital.nhs.uk/developer/help-and-support'
    new_dict['organisation'] = 'NHS Digital'
    new_dict['documentation-url'] = url
    return new_dict


# construction of the function
def get_list_of_dicts():
    filtered_list = []
    URL = 'https://digital.nhs.uk/developer/api-catalogue'
    api_urls = get_url_title(URL)
    for apis in api_urls:
        megadict = get_api_info(apis)
        initial_dict = create_filtered_dict(apis, megadict)
        filtered_list.append(initial_dict)

    return filtered_list

if __name__ == '__main__':
    get_list_of_dicts()

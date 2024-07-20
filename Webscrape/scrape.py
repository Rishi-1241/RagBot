import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_and_parse_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.content, 'html.parser')
    else:
        raise Exception(f"Failed to fetch the URL: {url}")

def extract_headings_with_content(soup):
    content = []
    for header in soup.find_all(['h1', 'h2', 'h3']):
        heading_text = header.get_text(strip=True)
        paragraphs = []
        for sibling in header.find_next_siblings():
            if sibling.name in ['h1', 'h2', 'h3']:
                break
            if sibling.name in ['p', 'div', 'ul', 'ol']:
                paragraphs.append(sibling.get_text(strip=True, separator='\n'))
        content.append((heading_text, '\n'.join(paragraphs)))
    return content

def extract_specific_div_content(soup):
    divs = soup.find_all('div', class_='refundPolicy')
    return [div.get_text(strip=True, separator='\n') for div in divs]

def extract_urls(soup, base_url):
    urls = []
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if not any(href.endswith(ext) for ext in ['.jpeg', '.jpg', '.png', '.svg']):
            urls.append(urljoin(base_url, href))
    return urls

def format_extracted_content(headings_content, div_content, urls):
    formatted_content = []
    
    for heading, content in headings_content:
        formatted_content.append(f"{heading}\n{content}\n")
    
    for div in div_content:
        formatted_content.append(f"Refund Policy Content:\n{div}\n")
    
    formatted_content.append("Extracted URLs:")
    formatted_content.extend(urls)
    
    return '\n'.join(formatted_content)

def main():
    url = 'https://lawsikho.com/course/diploma-in-us-corporate-law-and-paralegal-studies'
    soup = fetch_and_parse_url(url)
    
    headings_content = extract_headings_with_content(soup)
    div_content = extract_specific_div_content(soup)
    urls = extract_urls(soup, url)
    
    formatted_content = format_extracted_content(headings_content, div_content, urls)
    
    with open('datafile.txt', 'w', encoding='utf-8') as file:
        file.write(formatted_content)

main()

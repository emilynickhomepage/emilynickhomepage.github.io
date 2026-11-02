import os
import random
import re
import urllib.request

def get_top_story_link(url, regex_pattern):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Upgrade-Insecure-Requests': '1'
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            html_data = response.read().decode('utf-8', errors='ignore')
        match = re.search(regex_pattern, html_data)
        if match:
            return match.group(1)
    except Exception:
        pass
    return url

def main():
    stute_pattern = r'href="(https://thestute\.com/\d{4}/\d{2}/\d{2}/[^"]+)"'
    lafayette_pattern = r'<article class="news_results_block">\s*<a href="(https://news\.lafayette\.edu/\d{4}/\d{2}/\d{2}/[^"]+)"'
    
    stute_url = get_top_story_link("https://thestute.com/", stute_pattern)
    lafayette_url = get_top_story_link("https://news.lafayette.edu/", lafayette_pattern)

    valid_ext = ('.webp', '.jpg', '.jpeg', '.png', '.gif')
    images = [f for f in os.listdir('img') if f.lower().endswith(valid_ext)]
    selected_images = random.sample(images, 5) 

    with open('template.html', 'r', encoding='utf-8') as f:
        html = f.read()

    html = html.replace('{{STUTE_URL}}', stute_url)
    html = html.replace('{{LAFAYETTE_URL}}', lafayette_url)
    for i in range(5):
        html = html.replace(f'{{{{IMAGE_{i+1}}}}}', selected_images[i])

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == "__main__":
    main()

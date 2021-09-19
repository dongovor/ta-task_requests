
import requests, re, json, config, utils

from requests.models import Response

cookies_and_headers = []

#Preapare cookies and
def get_cookies_and_headers():
    r = requests.get(config.main_url)
    cookie = get_cookies(r.cookies, config.main_url.split('/')[-1])
    print(cookie)

    cookies = {
        cookie[0].split('=')[0] : cookie[0].split('=')[-1],
        'has_js': '1',
        'wstact': cookie[1].split('=')[1],
    }
    
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'sec-ch-ua': '^\\^Google',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Session-Token': cookie[1].split('=')[1],
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        'sec-ch-ua-platform': '^\\^Windows^\\^',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://itdashboard.gov/',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    cookies_and_headers.extend([headers, cookies])
    return cookies_and_headers

def get_cookies(cookie_jar, domain):
    cookie_dict = cookie_jar.get_dict(domain=domain)
    found = ['%s=%s' % (name, value) for (name, value) in cookie_dict.items()]
    return found


def collect_data(headers, cookies):
    response = requests.get(config.req_url, headers=headers, cookies=cookies)
    return response.text


def get_agency_info(headers, cookies, agencies_info):
    response = requests.get(config.agency_info_url.replace('agency_code', utils.get_agency_code(agencies_info)), headers=headers, cookies=cookies)
    return response.text

def get_PDF(headers, cookies, uii):
    response = requests.get(f"https://itdashboard.gov/api/v1/ITDB2/businesscase/pdf/generate/uii/{uii}", headers=headers, cookies=cookies)
    with open(f".\{config.path_to_save}\{uii}.pdf", 'wb') as f:
        f.write(response.content)

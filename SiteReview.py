import base64
import calendar
import inspect
import json
import os
import time

import pytesseract
import requests
import requests.auth
from PIL import Image
from getpass import getpass
from requests.exceptions import ProxyError

# defining an exception for wrong top-level domain error
class WrongTLD(Exception):
    def __init__(self, message="Wrong Top-Level Domain"):
        self.message = message
        super().__init__(self.message)


class SiteReview:
    def __init__(self,username,password):
        self.proxyDict = { 
                "http"  : 'http://'+username+':'+password+'@proxy_ip:proxy_port'
                "https"  : 'https://'+username+':'+password+'@proxy_ip:proxy_port'
        }
    
    # headers for requests
    headers = {
        'authority': 'sitereview.bluecoat.com',
        'accept': 'application/json, text/plain, */*',
        'x-xsrf-token': 'ce6e0505-ed4b-43ef-9624-9a5ad3b70f27',
        'accept-language': 'en',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        'content-type': 'application/json; charset=UTF-8',
        'origin': 'https://sitereview.bluecoat.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://sitereview.bluecoat.com/',
        'cookie': 'JSESSIONID=FD00E4699288139952D7B9CF25DC6F61; XSRF-TOKEN=ce6e0505-ed4b-43ef-9624-9a5ad3b70f27',
    }

    # special headers for reCaptcha
    _headers = {
        'authority': 'sitereview.bluecoat.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'accept': 'image/avif,image/webp,image/apng,image/*,*/*;q=0.8',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-dest': 'image',
        'referer': 'https://sitereview.bluecoat.com/',
        'accept-language': 'en-US;q=0.8,en;q=0.7',
        'cookie': 'JSESSIONID=FD00E4699288139952D7B9CF25DC6F61; XSRF-TOKEN=ce6e0505-ed4b-43ef-9624-9a5ad3b70f27; __utma=265713933.443691065.1605382266.1605382266.1605382266.1; __utmc=265713933; __utmz=265713933.1605382266.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    }

    # get decoded captcha answer
    def __get_captcha_base64(self):
        epoch_timestamp = str(calendar.timegm(time.gmtime()) * 1000)
        captcha_url = 'http://sitereview.bluecoat.com/resource/captcha.jpg?%s' % (epoch_timestamp)
        local_filename = 'captcha.jpg'
        r = requests.get(captcha_url, headers=self._headers, stream=True, proxies=self.proxyDict)
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        tesseract_dir = current_dir + r'\pytesseract\tesseract.exe'
        pytesseract.pytesseract.tesseract_cmd = tesseract_dir
        captcha = pytesseract.image_to_string(Image.open('captcha.jpg'))
        captcha = "".join(captcha.split())
        os.remove('captcha.jpg')

        captcha_utf = captcha.encode("UTF-8")
        base64_captcha = base64.b64encode(captcha_utf)
        return base64_captcha.decode("utf-8")

    # create data for request with specific URL
    def __get_data(self, url: str):
        return json.dumps(
            {"url": url, "captcha": "", "key": "f69e0635f42170328ee88fac4276ffb17a587931f2cd31ad0bdd2759005e0cc2",
             "phrase": "U2NyaXB0aW5nIGFnYWluc3QgU2l0ZSBSZXZpZXcgaXMgYWdhaW5zdCB0aGUgU2l0ZSBSZXZpZXcgVGVybXMgb2YgU2VydmljZQ==",
             "source": ""})

    # send captcha answer
    def __captcha_recognize(self):
        captcha = self.__get_captcha_base64()
        response = requests.get(f'http://sitereview.bluecoat.com/resource/captcha-request/{captcha}',
                                headers=self._headers, proxies=self.proxyDict)

    # if names_only == True -> get only category names from answer dictionaries
    def __get_names_only(self, categories):
        answers = []
        for answer in categories:
            category_name = answer['name']
            answers.append(category_name)
        return answers

    def get_category(self, url: str, names_only=True, is_again=False) -> list:
        data = self.__get_data(url)
        response = requests.post('http://sitereview.bluecoat.com/resource/lookup', headers=self.headers, data=data, proxies=self.proxyDict)
        #print(response.text)
        if response.status_code == 200:
            if names_only:
                return self.__get_names_only(json.loads(response.text)['categorization'])
            return json.loads(response.text)['categorization']
        # Check for captcha check
        if json.loads(response.text)['errorType'] == 'captcha':
            #print('[!] '+json.loads(response.text)['errorMessage'])
            print('[*] Solving Captcha... | ', end='')
            self.__captcha_recognize()
            return self.get_category(url, is_again=True)
        # Check for badurl (WrongTLD)
        if json.loads(response.text)['errorType'] == 'badurl':
            #print('[!] '+json.loads(response.text)['errorMessage'])
            raise WrongTLD
        # this condition is required for every 10th request
        elif not is_again:
            self.__captcha_recognize()
            return self.get_category(url, is_again=True)
        # this condition is required when user's IP is temporarily blocked by SiteReview
        else:
            time.sleep(5)
            self.__captcha_recognize()
            return self.get_category(url, is_again=True)


# Logic
try:
    user = input('Enter your username: ')
    passwd = getpass('Enter your password: ')
    categorizer = SiteReview(username=user,password=passwd)

    blocked_categories = ['Malicious Outbound Data/Botnets',
                            'Malicious Sources/Malnets',
                            'Phishing','Pornography',
                            'Potentially Unwanted Software',
                            'Spam','Suspicious']

    # Read from File
    with open('iocs.txt','r') as iocs_file:
        with open('iocs_result.txt', 'w') as iocs_result:
            for ioc in iocs_file:
                ioc = ioc.strip().replace('[.]','.').replace('[:]',':').replace('hxxp','http')
                try:
                    cat = categorizer.get_category(ioc, names_only=True)
                    print(ioc, cat)
                    if cat[0] not in blocked_categories:
                        #print(f'{ioc}:{cat}')
                        iocs_result.write(f'{ioc}\n')
                except WrongTLD:
                    print(f'[!] Wrong domain for {ioc}')
                    #iocs_result.write(f'[!] Wrong domain for {ioc}\n')
                except ProxyError as e:
                    print(e)
                    break
    print('Please, Check the output file called ./iocs_result.txt')
except KeyboardInterrupt:
    print('\n[!] Terminating Bluecoat Checker Script')
    exit(1)

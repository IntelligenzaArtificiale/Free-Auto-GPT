from re        import findall
from json      import loads, dumps
from queue     import Queue, Empty
from datetime  import datetime
from threading import Thread

from urllib.parse       import quote
from curl_cffi.requests import post


class Search:
    def create(prompt: str, actualSearch: bool = True, language: str = 'en') -> dict: # None = no search
        if not actualSearch:
            return {
                '_type': 'SearchResponse',
                'queryContext': {
                    'originalQuery': prompt
                },
                'webPages': {
                    'webSearchUrl' : f'https://www.bing.com/search?q={quote(prompt)}',
                    'value'        : [],
                    'totalEstimatedMatches': 0
                },
                'rankingResponse': {
                    'mainline' : {
                        'items': []
                    }
                }
            }
        
        headers = {
            'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'authority'    : 'www.phind.com',
            'origin'       : 'https://www.phind.com',
            'referer'      : 'https://www.phind.com/search',
            'user-agent'   : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        }
        
        return post('https://www.phind.com/api/bing/search', headers=headers, json = { 
            'q': prompt,
            'userRankList': {},
            'browserLanguage': language}).json()['rawBingResults']


class Completion:
    message_queue    = Queue()
    stream_completed = False
    
    def request(model, prompt, results, creative, detailed, codeContext, language) -> None:
        
        models = {
            'gpt-4' : 'expert',
            'gpt-3.5-turbo' : 'intermediate',
            'gpt-3.5': 'intermediate',
        }

        json_data = {
            'question'    : prompt,
            'bingResults' : results,
            'codeContext' : codeContext,
            'options': {
                'skill'   : models[model],
                'date'    : datetime.now().strftime("%d/%m/%Y"),
                'language': language,
                'detailed': detailed,
                'creative': creative
            }
        }
        
        stream_req = post('https://www.phind.com/api/infer/answer', json=json_data, timeout=99999,
            content_callback = Completion.handle_stream_response,
            headers = {
                'authority'    : 'www.phind.com',
                'origin'       : 'https://www.phind.com',
                'referer'      : f'https://www.phind.com/search?q={quote(prompt)}&c=&source=searchbox&init=true',
                'user-agent'   : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        })

        Completion.stream_completed = True

    @staticmethod
    def create(
        model       : str = 'gpt-4', 
        prompt      : str = '', 
        results     : dict = None, 
        creative    : bool = False, 
        detailed    : bool = False, 
        codeContext : str = '',
        language    : str = 'en'):
        
        if results is None:
            results = Search.create(prompt, actualSearch = True)
        
        if len(codeContext) > 2999:
            raise ValueError('codeContext must be less than 3000 characters')
        
        Thread(target = Completion.request, args=[model, prompt, results, creative, detailed, codeContext, language]).start()
        
        while Completion.stream_completed != True or not Completion.message_queue.empty():
            try:
                message = Completion.message_queue.get(timeout=0)
                print(message)
                for token in findall(r'(?<=data: )(.+?)(?=\r\n\r\n)', message.decode()):
                    yield token
                
            except Empty:
                pass

    @staticmethod
    def handle_stream_response(response):
        Completion.message_queue.put(response)

if __name__ == '__main__':
    array = ''
    
    for message in Completion.create(model='gpt-3.5-turbo', prompt='what is the meaning of life'):
        print(message)
        array += message
        
    print('\n\n' + array)

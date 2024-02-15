from html.parser import HTMLParser
import logging as log

log.basicConfig(level=log.DEBUG, filename='ehtmlparser.log')


class EHTMLParser(HTMLParser):
    def __init__(self, term):
        super().__init__()
        self.term = term

        self.tags = []
        self.style = {
            'h1': term.bold_black_on_red,
            'h2': term.bold_black_on_red,
            'h3': term.bold_black_on_red,
            'h4': term.bold_black_on_red,
            'h5': term.bold_black_on_red,
            'h6': term.bold_black_on_red,
            'p': term.black_on_white,
        }

        # a list of data strings and formatted escape sequences
        self.parsed_text = []


    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)


    def handle_endtag(self, tag):
        if len(self.tags) <= 0:
            log.debug('self.tags: %s, current tag: %s', self.tags, tag)
            return
        self.tags.pop()


    def handle_data(self, data):
        if self.style.get(self.tags[-1] if len(self.tags) > 0 else 'nothing'):
            self.parsed_text.append(self.style.get(self.tags.pop()))
            self.parsed_text.append(data)
            self.parsed_text.append(self.term.normal)
            return
        self.parsed_text += data


# parser = EHTMLParser()
# parser.feed('<html><head><title>Test</title></head>'
#             '<body class="con"><h1>Parse me!</h1><img src="image.png" /></body></html>')

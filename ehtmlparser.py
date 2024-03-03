from html.parser import HTMLParser
import logging as log


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
            '*': term.black_on_blue
        }

        # a list of data strings and formatted escape sequences
        self.parsed_text = []


    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        # style_key = self.tags[-1] if self.style.get(self.tags[-1] if len(self.tags) > 0 else 'notag') else '*'
        style = self.style.get(tag)
        if style:
            self.parsed_text.append(style)


    def handle_endtag(self, tag):
        if len(self.tags) > 0:
            # log.debug('self.tags: %s, current tag: %s', self.tags, tag)
            self.tags.pop()


    def handle_data(self, data):
        self.parsed_text.append(data)
        self.parsed_text.append(self.term.normal)


# parser = EHTMLParser()
# parser.feed('<html><head><title>Test</title></head>'
#             '<body class="con"><h1>Parse me!</h1><img src="image.png" /></body></html>')

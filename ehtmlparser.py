from html.parser import HTMLParser


class EHTMLParser(HTMLParser):
    def __init__(self, term):
        super().__init__()

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


    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)


    def handle_endtag(self, tag):
        self.tags.pop()


    def handle_data(self, data):
        if self.style.get(tags[-1]):
            self.text += '<seq>' self.style.get(self.tags.pop()) + '</seq>' + data + '<seq>' + self.term.normal + '</seq>'
            return
        self.text += data


parser = EHTMLParser()
parser.feed('<html><head><title>Test</title></head>'
            '<body class="con"><h1>Parse me!</h1><img src="image.png" /></body></html>')

from html.parser import HTMLParser


class EHTMLParser(HTMLParser):
    def __init__(self, term):
        super().__init__()
        self.term = term

        self.tags = []
        self.style = {
            'h1': term.black_on_red,
            'h2': term.black_on_red,
            'h3': term.black_on_red,
            'h4': term.black_on_red,
            'h5': term.black_on_red,
            'h6': term.black_on_red,
            'p': ''
        }
        self.open_tag = ''

        self.valid_data = False

        # a list of data strings and formatted escape sequences
        self.parsed_text = []


    def handle_starttag(self, tag, attrs):
        if not self.is_tag_valid(tag):
            return
        self.valid_data = True
        self.open_tag = tag
        self.parsed_text.append(self.style[tag])


    def handle_endtag(self, tag):
        if tag != self.open_tag:
            return

        # reset the open_tag and data
        self.open_tag = ''
        self.valid_data = False

        # appending newline after the previous dataline 'cause previous tag is closed
        self.parsed_text[-1] += '\n\n'

        # reset previous terminal style
        self.parsed_text.append(self.term.normal)


    def handle_data(self, data):
        if self.valid_data:
            self.parsed_text.append(data)


    def is_tag_valid(self, tag):
        """
        Checks if the tag is present in the style dict or not
        """
        return tag in self.style.keys()


    def clear(self):
        """
        Clears the current parsed text of parser
        """

        self.parsed_text = []


    def get_parsed_text(self):
        """
        Returns the current parsed_text list
        """
        return self.parsed_text


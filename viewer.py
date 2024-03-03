from math import ceil
from blessed import Terminal
from blessed.keyboard import Keystroke
import logging as log

from reader import Reader
from ehtmlparser import EHTMLParser

log.basicConfig(level=log.DEBUG, filename='epub_reader.log', filemode='w')

class View:
    def __init__(self, scr, width=0, height=0):
        self.scr = scr

        self.vw = width
        self.vh = height

        if (width == 0 or width > scr.width - 2) and (height == 0 or height > scr.height - 2):
            # substracting 2 to get the space to draw box around the view
            self.vw = scr.width - 2
            self.vh = scr.height - 2

        self.hc = ceil(self.scr.width / 2) - ceil(self.vw / 2)
        self.vc = ceil(self.scr.height / 2) - ceil(self.vh / 2)

        self.__boxes = [
            ['*', '*', '*', '*', '-', '|'],
            ['┌', '┐', '┘', '└', '─', '│'],
            ['┏', '┓', '┛', '┗', '━', '┃'],
            ['╔', '╗', '╝', '╚', '═', '║'],
            ['╭', '╮', '╯', '╰', '─', '│'],
            ['', ' ', ' ', ' ', ' ', '']
        ]

        self.box = self.__boxes[1]


    def drawBox(self):
        '''
        Draws a box around the view.
        '''

        # substracting 1 cause x,y are the cordinates of the view
        x = self.hc - 1
        y = self.vc - 1
        cords = [(x, y), (x + self.vw + 1, y), (x + self.vw + 1, y + self.vh + 1), (x, y + self.vh + 1)] # cordinates of the four corners
        i = 0
        for cord in cords:
            with self.scr.location(*cord):
                print(self.box[i], end = '')
                i += 1

        for i in range(x+1, x + self.vw + 1):
            with self.scr.location(i, y):
                print(self.box[4], end = '')
            with self.scr.location(i, y + self.vh + 1):
                print(self.box[4], end = '')

        for i in range(y+1, y + self.vh + 1):
            with self.scr.location(x, i):
                print(self.box[5], end = '')
            with self.scr.location(x + self.vw + 1, i):
                print(self.box[5], end = '')


    def printView(self, viewLines):
        self.drawBox()
        for i, line in enumerate(viewLines):
            with self.scr.location(self.hc, i + self.vc):
                print(line, end = '')


class Viewer:
    def __init__(self):
        self.scr = Terminal()
        self.r = Reader('ebook.epub')
        self.parser = EHTMLParser(self.scr)
        # self.vw = self.scr.width
        # self.vh = self.scr.height

        self.v = View(self.scr, 0, 0)

        self.vw = self.v.vw
        self.vh = self.v.vh

        self.cur = 0 # reading-cursor position line wise

        # self.chapter = self.chapterToLines(chapter_text)
        self.chapter = []
        self.totalLines = len(self.chapter)


    def setChapter(self, chapter_text):
        '''
        Takes chapter text as input and converts it into viewable lines
        of length equal to view width.
        '''

        if not chapter_text:
            return

        self.chapter = self.chapterToLines(chapter_text)
        self.totalLines = len(self.chapter)
        self.cur = 0


    def chapterToLines(self, text):
        viewLines = []
        vs = ''
        vl = 0 # length of vs without escape sequences
        for line in text:
            if line[0] == '\x1b':
                vs += line
                continue
            for i, c in enumerate(line):
                vs += c
                vl += 1

                if c == '\n' or vl >= self.vw:
                    viewLines.append(vs)
                    vs = ''
                    vl = 0

        if vs:
            viewLines.append(vs)

        return viewLines


    def parse_html(self, html_text):
        '''
        HTML to text + style escape sequences
        '''
        self.parser.parsed_text = []
        self.parser.feed(html_text)
        return self.parser.parsed_text


    def clear(self):
        print(self.scr.home + self.scr.clear)


    def __scroll(self, lines):
        '''
        Scrolls @{scroll_lines} number of lines down
        or up if @{scroll_lines} is negative
        '''

        self.cur += lines

        # checking if the cursor is out of bound
        if self.cur < 0:
            self.cur = 0

        elif self.cur >= self.totalLines - self.vh + 2:
            self.cur = self.totalLines - self.vh + 2


    def scrollLineUp(self):
        '''
        Scrolls one line up in the view.
        '''

        self.__scroll(-1)


    def scrollLineDown(self):
        '''
        Scrolls one line down in the view.
        '''

        self.__scroll(1)


    def scrollPageUp(self):
        '''
        Scrolls one page up according to view height.
        '''
        self.__scroll(-self.vh)


    def scrollPageDown(self):
        '''
        Scrolls one page down according to view height.
        '''
        self.__scroll(self.vh)


    def nextChapter(self):
        ischap, chap = self.r.nextChapter()
        self.setChapter(self.parse_html(chap) if ischap else '')


    def prevChapter(self):
        ischap, chap = self.r.prevChapter()
        self.setChapter(self.parse_html(chap) if ischap else '')


    def printView(self):
        self.clear()
        # for i, line in enumerate(self.chapter[self.cur:self.cur + self.vh]):
        #     with self.scr.location(0, i):
        #         print(line, end = '')
        # print((self.scr.width, self.scr.height))
        self.v.printView(self.chapter[self.cur:self.cur + self.vh])


    def view(self):
        self.nextChapter()
        with self.scr.fullscreen(), self.scr.cbreak(), self.scr.hidden_cursor(), self.scr.raw():
            key = Keystroke()
            while True:
                match key:
                    case k if k in ['j', 'J']:
                        self.scrollLineDown()
                    case k if k in ['k', 'K']:
                        self.scrollLineUp()
                    case k if k in ['h', 'H']:
                        self.prevChapter()
                    case k if k in ['l', 'L']:
                        self.nextChapter()
                    case k if k in ['q', 'Q']:
                        break
                    case _:
                        # self.clear()
                        # with self.scr.location(50, 10):
                        #     print(f'name: {key.name}, code: {key.code}')
                        pass

                self.printView()
                key = self.scr.inkey()


v = Viewer()
# v.setChapter('\n'.join([f'This is chapter line {i}.' for i in range(100)]))
v.view()

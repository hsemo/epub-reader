from math import ceil
from blessed import Terminal


class Viewer:
    def __init__(self, chapter_text = ''):
        self.scr = Terminal()
        # self.vw = self.scr.width
        # self.vh = self.scr.height
        self.vw = 20
        self.vh = 10

        self.cur = 0 # reading-cursor position line wise

        self.chapter = self.chapterToLines(chapter_text)
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


    def chapterToLines(self, text):
        viewLines = []
        vs = ''
        i = 0
        for i, c in enumerate(text):
            vs += c

            if c == '\n' or len(vs) >= self.vw:
                viewLines.append(vs)
                vs = ''

        if vs:
            viewLines.append(vs)

        return viewLines


    # def calcChapLines(self):
    #     '''
    #     Calculates chapter lines
    #     '''
    #
    #     lines = 0
    #     p = 0 # previous position of newLine char
    #     for i,c in enumerate(self.chapter):
    #         if c == '\n':
    #             lines += ceil((i - p) / self.vw)
    #             p = i
    #
    #     if lines == 0:
    #         lines = ceil(len(self.chapter) / self.vw)
    #     return lines


    def clear(self):
        print(self.scr.home + self.scr.clear)


    def __scroll(self, lines):
        '''
        Scrolls @{scroll_lines} number of lines down
        or up if @{scroll_lines} is negative
        '''

        self.cur += lines

        # checking if the cursor is out of bound
        self.cur = 0 if self.cur < 0 else self.cur

        if self.cur >= self.totalLines - self.vh + 2:
            self.cur = self.totalLines - self.vh + 2

    # def __scroll(self, scroll_lines):
    #     '''
    #     Scrolls @{scroll_lines} number of lines down
    #     or up if @{scroll_lines} is negative
    #     '''
    #
    #     if scroll_lines == 0:
    #         return
    #     elif scroll_lines < 0:
    #         s = self.chapter[self.cur-1::-1]
    #     else:
    #         s = self.chapter[self.cur:]
    #
    #     viewLines = 0
    #     vs = 0
    #     i = 0
    #     for i, c in enumerate(s):
    #         if viewLines >= scroll_lines:
    #             break
    #
    #         vs += 1
    #
    #         if c == '\n' or vs >= self.vw:
    #             viewLines += 1
    #             vs = 0
    #
    #     self.cur += i if scroll_lines > 0 else i * -1
    #     self.cur = 0 if self.cur < 0
    #     self.cur = len(self.chapter) - 1 if self.cur >= len(self.chapter)


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


    def printView(self):
        # viewLines = []
        # vs = ''
        # for c in self.chapter[self.cur:]:
        #     if len(viewLines) >= self.vh:
        #         break
        #
        #     vs += c
        #
        #     if c == '\n' or len(vs) >= self.vw:
        #         viewLines.append(vs)
        #         vs = ''

        self.clear()
        for i, line in enumerate(self.chapter[self.cur:self.cur + self.vh]):
            with self.scr.location(0, i):
                print(line, end = '')


    def view(self):
        with self.scr.fullscreen(), self.scr.cbreak(), self.scr.hidden_cursor():
            key = ''
            while True:
                match key:
                    case k if k in ['j', 'J']:
                        self.scrollLineDown()
                    case k if k in ['k', 'K']:
                        self.scrollLineUp()
                    case k if k in ['h', 'H']:
                        self.scrollPageUp()
                    case k if k in ['l', 'L']:
                        self.scrollPageDown()
                    case k if k in ['q', 'Q']:
                        break
                    case _:
                        pass

                self.printView()
                key = self.scr.inkey()


v = Viewer()
v.setChapter('\n'.join([f'This is chapter line {i}.' for i in range(100)]))
v.view()

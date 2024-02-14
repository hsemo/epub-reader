import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup as bs


# book = epub.read_epub('ebook.epub')
# chapters = [book.get_item_with_id(item[0]) for item in book.spine]


class Reader:
    def __init__(self, bpath):
        self.book = epub.read_epub(bpath)
        self.chapters = [self.book.get_item_with_id(item[0]) for item in self.book.spine]
        self.currentChapIndex = -1


    def __getText(self, chap):
        soup = bs(chap.get_content().decode())

        # with open("chapter_html.html", 'w') as f:
        #     f.write(chap.get_content().decode())

        chap_text = soup.find_all('body')[0].get_text()

        # with open("chapter_text.txt", 'w') as f:
        #     f.write(chap_text)

        return chap_text

    def nextChapter(self):
        '''
        Returns the next chapter of the book as string.
        '''

        self.currentChapIndex += 1
        if self.currentChapIndex >= len(self.chapters):
            self.currentChapIndex = len(self.chapters) - 1
            return (False, None,)

        return (True, self.__getText(self.chapters[self.currentChapIndex]),)


    def prevChapter(self):
        '''
        Returns the previous chapter of the book as string.
        '''

        self.currentChapIndex -= 1
        if self.currentChapIndex < 0:
            self.currentChapIndex = -1
            return (False, None)

        return (True, self.__getText(self.chapters[self.currentChapIndex]))



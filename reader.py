import logging as log

import ebooklib
from ebooklib import epub


class Reader:
    def __init__(self, bpath):
        self.book = epub.read_epub(bpath)
        self.items = [self.book.get_item_with_id(item[0]) for item in self.book.spine]
        log.debug("Total items: %s", len(self.items))
        self.currentChapIndex = -1


    def __getText(self, chap):
        return chap.get_content().decode()

    def nextChapter(self):
        '''
        Returns the next chapter of the book as string.
        '''

        self.currentChapIndex += 1
        if self.currentChapIndex >= len(self.items):
            self.currentChapIndex = len(self.items) - 1
            return (False, None,)

        log.debug("nextChapter - Going to chapter: %s", self.currentChapIndex)
        return (True, self.__getText(self.items[self.currentChapIndex]),)


    def prevChapter(self):
        '''
        Returns the previous chapter of the book as string.
        '''

        self.currentChapIndex -= 1
        if self.currentChapIndex < 0:
            self.currentChapIndex = -1
            return (False, None)

        log.debug("prevChapter - Going to chapter: %s", self.currentChapIndex)
        return (True, self.__getText(self.items[self.currentChapIndex]))



import spriteling, spells

class player(spriteling.active):
    def __init__(self, *args):
        super().__init__(*args)



class multiplayer(player):
    def __init__(self, number, book, *args):
        self.player_number = number
        if number == 1:
            self.book_slot = 'top left corner of the screen'
        elif number == 2:
            self.book_slot = 'top right corner'
        elif number == 3:
            self.book_slot = 'bottom left'
        elif number == 4:
            self.book_slot = 'bottom right'

        self.spellbook = book(self)

        self.spell_slot = self.rect.center
        self.cast_point = self.rect.center

        # this is temporary. a testing setup
        self.image = self.spellbook.image



class soloplayer(player):
    def __init__(self, *args):
        super().__init__(*args)
import json
import os
import re


class TextCleanUp:
    def __init__(self):
        ps_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            './parsing_symbols.json')
        
        with open(ps_file, 'r') as f:
            self.symbols_table = json.loads(f.read())

    def cleanup_text(self, text, ignore=()):
        """
        Original author: Olga Kononova.

        :param text:
        :return: Cleaned text.
        :rtype: str
        """
        quotes_double = [171, 187, 8220, 8221, 8222, 8223]
        quotes_single = [8216, 8217, 8218, 8219, 8249, 8250]
        hyphens = [8722] + [i for i in range(8208, 8214)]
        times = [183, 215, 8729]
        spaces = [i for i in range(8192, 8208)] + [8239, 8287]
        formating = [i for i in range(8288, 8304)] + \
                    [i for i in range(8232, 8239)]
        math = [i for i in range(8592, 8961)]
        modifiers = [i for i in range(688, 768)] + \
                    [i for i in range(7468, 7531)] + \
                    [i for i in range(7579, 7616)]
        combining = [i for i in range(768, 880)] + \
                    [i for i in range(1156, 1162)] + \
                    [i for i in range(7616, 7680)] + \
                    [i for i in range(8400, 8433)]
        control = [i for i in range(32)] + \
                  [i for i in range(127, 160)]

        new_text = text

        for c in ['†']:
            if c not in ignore:
                new_text = new_text.replace(c, '')

        for c in self.symbols_table:
            if c not in ignore:
                new_text = new_text.replace(c, self.symbols_table[c])

        for c in quotes_double:
            if chr(c) not in ignore:
                new_text = new_text.replace(chr(c), '"')

        for c in quotes_single:
            if chr(c) not in ignore:
                new_text = new_text.replace(chr(c), '\'')

        for c in hyphens:
            if chr(c) not in ignore:
                new_text = new_text.replace(chr(c), '-')

        # for c in times:
        #    text = text.replace(chr(c), '*')

        for c in spaces:
            if chr(c) not in ignore:
                new_text = new_text.replace(chr(c), chr(32))

        for c in formating:
            if chr(c) not in ignore:
                new_text = new_text.replace(chr(c), chr(32))

        new_text = new_text.replace(chr(160), '')
        new_text = new_text.replace(chr(173), '')  # soft hyphen
        #new_text = re.sub('(\d+),(\d+)', '\\1\\2', new_text) #remove coma in thousands
        # text = re.sub('\d+(\+)\d+', ' + ', text)
        new_text = re.sub('(\w+)=(\d+)', '\\1 = \\2', new_text)
        new_text = new_text.replace('%', '% ')
        new_text = new_text.replace(' )', ')')
        new_text = re.sub('\s+,', ',', new_text)
        new_text = re.sub(',', ', ', new_text)
        new_text = re.sub('\(\s+', '(', new_text)
        new_text = re.sub(' {2,}', ' ', new_text)
        new_text = new_text.replace('° C', '°C')

        return new_text

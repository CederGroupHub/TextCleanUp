# coding=utf-8
import json
import os
import re


class TextCleanUp:
    def __init__(self):
        print('Text Cleanup version 2.5')
        ps_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'parsing_symbols.json')

        #ps_file = "/home/olga/PycharmProjects/CederGroup_IMaSynProject/TextCleanUp/text_cleanup/parsing_symbols.json"
        
        with open(ps_file, 'r') as f:
            self.symbols_table = json.loads(f.read())

    def cleanup_text(self, text, ignore=[]):
        """
        Original author: Olga Kononova.

        :param ignore:
        :param text:
        :return: Cleaned text.
        :rtype: str
        """
        quotes_double = [171, 187, 8220, 8221, 8222, 8223, 8243]
        quotes_single = [8216, 8217, 8218, 8219, 8242, 8249, 8250]
        #hyphens = [8722] + [i for i in range(8208, 8214)]
        hyphens = [173, 8722, ord('\ue5f8'), 727, 12287, 12257] + [i for i in range(8208, 8214)]
        times = [183, 215, 8729]
        spaces = [i for i in range(8192, 8208)] + [160, 8239, 8287,61472]
        formating = [i for i in range(8288, 8298)] + [i for i in range(8299, 8304)] + [i for i in range(8232, 8239)]
        degrees = [186, 730, 778, 8304, 8728, 9702, 9675]
        # math = [i for i in range(8592, 8961)]
        # modifiers = [i for i in range(688, 768)] + \
        #             [i for i in range(7468, 7531)] + \
        #             [i for i in range(7579, 7616)]
        # combining = [i for i in range(768, 880)] + \
        #             [i for i in range(1156, 1162)] + \
        #             [i for i in range(7616, 7680)] + \
        #             [i for i in range(8400, 8433)]
        # control = [i for i in range(32)] + \
        #           [i for i in range(127, 160)]

        to_remove = [775, 8224, 8234, 8855, 8482, 9839]

        # 8289

        # remove 8298 and next symbol
        # replace 12289 with coma

        new_text = text

        for c in self.symbols_table:
            new_text = new_text.replace(c, self.symbols_table[c])

        # hyphens unification
        re_str = ''.join([chr(c) for c in hyphens if c not in ignore])
        re_str = '[' + re_str + ']'
        new_text = re.sub(re_str, chr(45), new_text)

        #spaces unification
        re_str = ''.join([chr(c) for c in spaces if c not in ignore])
        re_str = '[' + re_str + ']'
        new_text = re.sub(re_str, chr(32), new_text)

        #quotes unification
        re_str = ''.join([chr(c) for c in quotes_single if c not in ignore])
        re_str = '[' + re_str + ']'
        new_text = re.sub(re_str, chr(39), new_text)

        re_str = ''.join([chr(c) for c in quotes_double if c not in ignore])
        re_str = '[' + re_str + ']'
        new_text = re.sub(re_str, chr(34), new_text)

        #formatting symbols
        re_str = ''.join([chr(c) for c in formating+to_remove if c not in ignore])
        re_str = '[' + re_str + ']'
        new_text = re.sub(re_str, '', new_text)

        #degrees
        re_str = ''.join([chr(c) for c in degrees if c not in ignore])
        re_str = '[' + re_str + ']'
        new_text = re.sub(re_str, chr(176), new_text)
        new_text = new_text.replace('° C', '°C')
        new_text = new_text.replace('°C', ' °C')

        new_text = re.sub('Fig.\s*([0-9]+)', 'Figure \\1', new_text)
        new_text = re.sub('[Rr]ef.\s*([0-9]+)', 'reference \\1', new_text)
        new_text = re.sub('\sal\.\s*[0-9\s]+', ' al. ', new_text)

        for c in [' Co.', 'Ltd.', 'Inc.', 'A.R.', 'Corp.', 'A. R.']:
            new_text = new_text.replace(c, '')
        new_text = new_text.replace('()', '')

        new_text = re.sub('\s+,', ',', new_text)
        new_text = re.sub('([1-9]),([0-9]{3})', '\\1\\2', new_text)  # remove coma in thousands
        new_text = re.sub('(\w+)=(\d+)', '\\1 = \\2', new_text)
        new_text = re.sub('\(\s+', '(', new_text)
        new_text = new_text.replace(' %', '%')
        new_text = new_text.replace(' )', ')')
        new_text = re.sub('(\d+),([A-Za-z])', '\\1, \\2', new_text)

        new_text = re.sub('\s{2,}', ' ', new_text)

        return new_text

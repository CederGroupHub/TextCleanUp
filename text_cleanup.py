import re
import json
import os
import pubchempy as pcp

class TextCleanUp:

    def __init__(self):
        ps_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            './parsing_symbols.json')

        self.symbols_table = json.loads(open(ps_file).read())

    def cleanup_text(self, text, ignore=[]):
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

    def clean_up_material_name(self, material_name, remove_offstoichiometry=False):

        """
        this is a fix of incorrect tokenization of chemical names
        do not rely much on it
        tested on specific sample of papers from 20K solid-state paragraphs
        use at your own risk
        :param
        material_name: string - initial material string
        remove_offstoichiometry: boolean - if True greek symbols next to O at the end of formula will be removed
        :return: string
        """

        updated_name = ''
        remove_list = ['SOFCs', 'LT-SOFCs', 'IT-SOFCs', '(IT-SOFCs']

        # this is mostly for precursors
        for c in ['\(99', '\(98', '\(90', '\(95', '\(96', '\(Alfa', '\(Aldrich', '\(A.R.', '\(Aladdin', '\(Sigma',
                  '\(A.G', '\(Fuchen', '\(Furuuchi', '(AR)']:
            material_name = re.split(c, material_name)[0]
        material_name = material_name.rstrip('(-')

        material_name = material_name.replace('(s)', '')

        # unifying hydrates representation
        dots = [8901, 8729, 65381, 120, 42, 215, 8226]
        if 'H2O' in material_name:
            for c in dots:
                material_name = material_name.replace(chr(c), chr(183))

        # symbols from phase... need to move it to phase section
        for c in ['″', '′', 'and']:
            material_name = material_name.replace(c, '')

        # leftovers from references
        for c in re.findall('\[[0-9]+\]', material_name):
            material_name = material_name.replace(c, '')

        # can be used to remove unresolved stoichiometry symbol at the end of the formula
        if remove_offstoichiometry and material_name != '':
            if material_name[-1] == 'δ' and len(re.findall('δ', material_name)) == 1:
                material_name = material_name[0:-1]
                material_name = material_name.rstrip('- ')

        # getting rid of trash words
        material_name = material_name.replace('ceramics', '')
        material_name = material_name.replace('ceramic', '')
        trash_words = ['bulk', 'coated', 'rare', 'earth', 'undoped', 'layered']
        for w in trash_words:
            material_name = material_name.replace(w, '')

        material_name = material_name.strip(' ')

        # standartize aluminium name
        material_name = material_name.replace('aluminum', 'aluminium')
        material_name = material_name.replace('Aluminum', 'Aluminium')

        if material_name in remove_list or material_name == '':
            return ''

        # make single from plurals
        if material_name != '':
            if material_name[-2:] not in ['As', 'Cs', 'Os', 'Es', 'Hs', 'Ds']:
                material_name = material_name.rstrip('s')

        # removing valency - that's not a good thing actually...
        # assuming that we have read this value on earlier stages
        material_name = re.sub('(\s*\([IV,]+\))', '', material_name)

        # checking if the name in form of "chemical name [formula]"
        if material_name[0].islower() and material_name[0] != 'x':
            parts = [s for s in re.split('([a-z\-\s]+)\s*\[(.*)\]', material_name) if s != '']
            if len(parts) == 2:
                return parts.pop()

        return material_name

import re
from pathlib import Path

import bs4
import numpy as np

def translator(string: str) -> str:
    t = np.random.randint(1, 43)
    pos = string.find('%1$@')
    if (pos != -1):
        pos += 4
        string = string[:pos] + ')' + string[pos:]
    pos = string.find('%1$s')
    if (pos != -1):
        pos += 4
        string = string[:pos] + ')' + string[pos:]
 
    if (t == 42):
        return string.rstrip('.') + '...)'
    return string.rstrip('.') + ')'
    


def translate_xml(text: str) -> str: 
    soup = bs4.BeautifulSoup(text, 'xml')

    for s in soup.find_all('string'):
        s.string = translator(s.string)

    return str(soup)


def translate_strings(text: str) -> str:
    def repl(match):
        return match.group(1) + translator(match.group(2)) + match.group(3)

    result, _ = re.subn(r'^(".+" = ")(.+)(";)$', repl, text, flags=re.MULTILINE)
    return result


def translate(path: Path = Path('translations')):
    path_original = path / 'original'
    path_dest = path / 'skobochka'

    print(f'Starting translation in path: {path_original}\n')

    for f_original in path_original.iterdir():
        print(f'   Processing: {f_original}')
        f_dest = path_dest / f_original.name.replace('_ru_', '_skobochka_')

        translation = f_original.read_text()
        result = translation

        if f_original.suffix == '.strings':
            result = translate_strings(translation)

        if f_original.suffix == '.xml':
            result = translate_xml(translation)

        print(f'Saving result: {f_dest}\n')
        f_dest.write_text(result)

    print('Finished!')


if __name__ == '__main__':
    translate()

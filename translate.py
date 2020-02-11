import re
from pathlib import Path
import numpy as np
import bs4


def translator(string: str) -> str:
    if (np.random.randint(1, 43) == 42):
        return string.rstrip('.') + ')'
    else: return string.rstrip('.') + '...)'


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

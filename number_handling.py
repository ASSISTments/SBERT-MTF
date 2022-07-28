import sys
import numpy as np
import num2words as n2w

number_names = None


def preLoadNumberNames(n=10000):
    global number_names
    if number_names is None:
        output_str = '-- loading {}...({}%)'.format('number names', 0)
        sys.stdout.write(output_str)
        sys.stdout.flush()
        old_str = output_str

        number_names = dict()
        for i in range(n):
            w = n2w.num2words(str(i)).lower().replace(',', '')

            number_names[w] = str(i)
            number_names[w.replace('-', ' ')] = str(i)
            number_names[w.replace(' and', '')] = str(i)
            number_names[w.replace('-', ' ').replace(' and', '')] = str(i)
            if i > 10 and w[:3] == 'one':
                aw = w.replace('one', 'a', 1)
                number_names[aw] = str(i)
                number_names[aw.replace('-', ' ')] = str(i)
                number_names[aw.replace(' and', '')] = str(i)
                number_names[aw.replace('-', ' ').replace(' and', '')] = str(i)

            if not round((i / n) * 100, 2) == round(((i - 1) / n) * 100, 2):
                sys.stdout.write('\r' + (' ' * len(old_str)))
                output_str = '\r-- loading {}...({}%)'.format('number names', round((i / n) * 100, 2))
                sys.stdout.write(output_str)
                sys.stdout.flush()
                old_str = output_str

        for i in range(10):
            w = n2w.num2words(str(i), to='ordinal').lower().replace(',', '')

            number_names[w] = str(i)

            if not round(((i + n) / (n + 10)) * 100, 2) == round((((i + n) - 1) / (n + 10)) * 100, 2):
                sys.stdout.write('\r' + (' ' * len(old_str)))
                output_str = '\r-- loading {}...({}%)'.format('number names', round(((i + n) / (n + 10)) * 100, 2))
                sys.stdout.write(output_str)
                sys.stdout.flush()
                old_str = output_str

        additional = ['dozen', 'half', 'half dozen', 'one third', 'one fourth', 'one tenth']
        additional_map = ['12', '.5', '6', '0.3333333333', '0.25', '0.1']
        for i in range(len(additional)):
            number_names[additional[i]] = additional_map[i]

        sys.stdout.write('\r' + (' ' * len(old_str)))
        sys.stdout.write('\r-- loading {}...({}%)\n'.format('number names', 100))
        sys.stdout.flush()


def replace_numbers_numerical(text):
    global number_names
    if number_names is None:
        preLoadNumberNames()

    text = str(text)
    k = np.argsort([len(i) for i in sorted(number_names.keys())])[::-1]
    for i in np.array(sorted(number_names.keys()))[k]:
        if text.find(i) != -1:
            text = text.replace(i, number_names[i])
            continue

    return text


if __name__ == '__main__':
    print(replace_numbers_numerical('one hundred'))

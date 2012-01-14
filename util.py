from glob import iglob
from os.path import splitext

def write_file_list(filename, file_list=[], glob=None):
    if glob:
        file_list = iglob(glob)

    with open(filename, 'w') as f:
        for line in file_list:
            f.write(line + '\n')


def file_variations(filename, extentions):
    (label, ext) = splitext(filename)
    return [label + extention for extention in extentions]

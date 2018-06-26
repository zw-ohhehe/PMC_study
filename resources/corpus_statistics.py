
import json
import os
import re


def format_structure(structures):
    is_complete = True
    is_empty = True
    for key, item in structures.items():
        if len(item) == 0:
            is_complete = False
        else:
            is_empty = False
    return {'structure': structures,
            'is_complete': is_complete,
            'is_empty': is_empty}


def parse_capital_title(data):
    structures = {'introduction': '',
                  'methods': '',
                  'results': '',
                  'discussion': ''
                  }

    try:
        body = data.split('==== Body')[1].split('====Refs')[0]
    except:
        return format_structure(structures)
    pattern = r'[A-Z_ ,]{5,}\n'
    titles = re.findall(pattern, body)
    contents = re.split(pattern, body)
    sections = {}

    # In case number of titles and contents are inconsistent.
    if len(titles) != len(contents) - 1:
        return None
    for i in range(len(titles)):
        sections[titles[i].split('/n')[0].lower()] = contents[i + 1]

    for key, value in sections.items():
        if 'introduction' in key:
            structures['introduction'] = value
        elif 'method' in key:
            structures['methods'] = value
        elif 'result' in key:
            if len(structures['results']) == 0:
                structures['results'] = value
            else:
                structures['results'] += value
        elif 'discussion' in key:
            if len(structures['discussion']) == 0:
                structures['discussion'] = value
            else:
                structures['discussion'] += value

    formatted_structure = format_structure(structures)
    if not formatted_structure['is_empty']:
        formatted_structure['is_capital_title'] = True
    return formatted_structure


def find_words(words, line):
    for word in words:
        if word in line[: len(word) + 5] or word.upper() in line[: len(word) + 5]:
            return True
    return False


def parse_paper(data):
    structures = {'introduction': '',
                  'methods': '',
                  'results': '',
                  'discussion': ''
                  }
    if '==== Body' in data:
        if '==== Refs' in data:
            body = data.split('==== Body')[1].split('==== Refs')[0]
        else:
            body = data.split('==== Body')[1]
    else:
        return format_structure(structures)

    lines = body.split('\n')
    state = ''
    for line in lines:
        if find_words(['Introduction', 'Background'], line):
            state = 'introduction'
        elif find_words(['Methods', 'Materials and methods', 'Materials and Methods'], line):
            state = 'methods'
        elif find_words(['Results'], line):
            state = 'results'
        elif find_words(['Conclusion', 'Discussion'], line):
            state = 'discussion'
        else:
            if len(state) > 0:
                structures[state] += line
    return format_structure(structures)


class Journal:
    def __init__(self, name, num_c, num_nc, num_us):
        self.papers = {'complete': num_c,
                       'non-complete': num_nc,
                       'non-structure': num_us}
        self.name = name

    def dominant(self):
        s = sum([v for k, v in self.papers.items()])
        for item, value in self.papers.items():
            if s > 0 and value / s > 1 / 3:
                return [self.name, item, value / s, s]
        return [self.name, item, 0, 0]


def load_file(path):
    num_files = 0
    num_complete = 0
    num_non_complete = 0
    num_unclassified = 0
    file_complete = []
    file_non_complete = []
    file_unstructure = []
    journals = []
    for folder in os.listdir(path):
        num_complete_journal = 0
        num_non_complete_journal = 0
        num_unstructure_journal = 0
        num_file_in_folder = len(os.listdir(os.path.join(path, folder)))
        for file_name in os.listdir(os.path.join(path, folder)):
            with open(os.path.join(path, folder, file_name), encoding='utf8') as f:
                data = f.read()
            parsed_result = parse_paper(data)
            if parsed_result['is_complete']:
                num_complete += 1
                file_complete.append(os.path.join(path, folder, file_name))
                num_complete_journal += 1
            elif not parsed_result['is_empty']:
                num_non_complete += 1
                file_non_complete.append(os.path.join(path, folder, file_name))
                num_non_complete_journal += 1
            else:
                num_unclassified += 1
                file_unstructure.append(os.path.join(path, folder, file_name))
                num_unstructure_journal += 1
            num_files += 1

        journal = Journal(folder, num_complete_journal, num_non_complete_journal, num_unstructure_journal)
        journals.append(journal.dominant())
        if num_file_in_folder > 100 and num_unstructure_journal / num_file_in_folder > 0.5:
            print('need review', folder)
    with open(os.path.join(os.getcwd(), 'results', 'journal_analysis.txt'), 'w') as f:
        for j in journals:
            f.write('{}\t{}\t{}\t{}\n'.format(j[0], j[1], j[2], j[3]))
    with open(os.path.join(os.getcwd(), 'results', 'file_name_complete.json'), 'w') as f:
        json.dump(file_complete, f)
    with open(os.path.join(os.getcwd(), 'results', 'file_name_non_complete.json'), 'w') as f:
        json.dump(file_non_complete, f)
    with open(os.path.join(os.getcwd(), 'results', 'file_name_unstructure.json'), 'w') as f:
        json.dump(file_unstructure, f)


if __name__ == '__main__':
    path = 'D:\PMC'
    #path = os.path.join(os.getcwd(), 'data')
    load_file(path)



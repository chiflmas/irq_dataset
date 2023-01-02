#!/usr/bin/env python3
import os
import bs4
import csv


def first_row(csv_file):
    """
    Writes first row with column headers.
    :param csv_file: path to .csv file to insert headers
    :return: .csv file with headers row
    """
    with open(csv_file, 'w', newline='') as f:
        write = csv.writer(f)
        write.writerow(['Region', 'Datetime', 'Type', 'Category', 'Affiliation',
                        'Detained', 'Enemy_KIA', 'Friend_KIA', 'Civilian_KIA', 'Host_nation_KIA',
                        'Enemy_WIA', 'Friend_WIA', 'Civilian_WIA', 'Host_nation_WIA', 'Complex_attack',
                        'Type_of_unit', 'MGRS'])


def html_parser(html_file, q):
    """
    Opens a html file and searches for items inside tables.
    :param html_file: sigact html file.
    :param q: queue object to save jobs pending to write
    :return: queue item
    """
    with open(html_file) as f:
        soup = bs4.BeautifulSoup(f, 'html.parser')
        tables = soup.find_all('table')
        fields = []
        index = [1, 4, 5, 6, 7, 8, 10, 11, 12, 13, 15, 16, 17, 18, 22, 25, 28]
        row_sigact = []
        codes = soup.find_all('code')
        for i in range(0, 3):
            for row in tables[i].find_all('tr'):
                for column in row.find_all('td'):
                    fields.append(column.get_text())
        for v in codes[1].strings:
            fields.append(v.split(':')[-1])
        for i in index:
            row_sigact.append(fields[i])
        q.put(row_sigact)


def listener(queue, csv_file):
    """
    Searches for rows pending to write inside a queue and writes them into a .csv file.
    If last job is last_job kills the listener.
    :param queue: queue with jobs pending to write.
    :param csv_file: path to .csv file to write rows
    :return: csv file
    """
    with open(csv_file, 'a', newline='') as f:
        write = csv.writer(f)
        while 1:
            row = queue.get()
            if row == 'last_row':
                break
            write.writerow(row)


def flat_sigact_files(root_folder):
    """
    Searches for html files in a folder tree and saves them into a list.
    :param root_folder: Parent folder of sigacts html files.
    :return: List with all the sigacts html file_names.
    """
    files_sigact = []
    for root, dirs, files in os.walk(root_folder):
        for name in files:
            files_sigact.append('\\'.join([root, name]))
    return files_sigact

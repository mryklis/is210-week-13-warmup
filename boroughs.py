#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""broughs data module"""

import csv
import json

GRADES = {'A': '100', 'B': '90', 'C': '80', 'D': '70', 'F': '60'}


def get_score_summary(file_name=''):
    """ This function sumamrizes the score and counts restaurant perboro

    Args:
        file_name (str): input csv file

    Returns:
        score_summary (dic): rest per boro summarized

    Example:
        >>> get_score_summary('inspection_results.csv')
        >>> {'BRONX': (156, 0.9762820512820514), 'BROOKLYN':
        (417, 0.9745803357314141), 'STATEN ISLAND': (46, 0.9804347826086955),
        'MANHATTAN': (748, 0.9771390374331531), 'QUEENS':
        (414, 0.9719806763285017)}
    """

    new_dict = {}

    with open(file_name, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            CAMIS, BORO, GRADE = (row[0], row[1], row[10])
            if CAMIS not in new_dict and GRADE != '' and GRADE != 'P':
                new_dict[CAMIS] = [BORO, GRADE]
    csvfile.close()

    man_count, man_score = 0, 0
    bkl_count, bkl_score = 0, 0
    bx_count, bx_score = 0, 0
    qns_count, qns_score = 0, 0
    si_count, si_score = 0, 0

    for value in new_dict.itervalues():
        if value[0] == 'BROOKLYN':
            bkl_count += 1
            if value[1] == 'A':
                score = float(GRADES.get('A'))
            elif value[1] == 'B':
                score = float(GRADES.get('B'))
            elif value[1] == 'C':
                score = float(GRADES.get('C'))
            elif value[1] == 'D':
                score = float(GRADES.get('D'))
            elif value[1] == 'F':
                score = float(GRADES.get('F'))
            bkl_score += score
        elif value[0] == 'QUEENS':
            qns_count += 1
            if value[1] == 'A':
                score = float(GRADES.get('A'))
            elif value[1] == 'B':
                score = float(GRADES.get('B'))
            elif value[1] == 'C':
                score = float(GRADES.get('C'))
            elif value[1] == 'D':
                score = float(GRADES.get('D'))
            elif value[1] == 'F':
                score = float(GRADES.get('F'))
            qns_score += score
        elif value[0] == 'MANHATTAN':
            man_count += 1
            if value[1] == 'A':
                score = float(GRADES.get('A'))
            elif value[1] == 'B':
                score = float(GRADES.get('B'))
            elif value[1] == 'C':
                score = float(GRADES.get('C'))
            elif value[1] == 'D':
                score = float(GRADES.get('D'))
            elif value[1] == 'F':
                score = float(GRADES.get('F'))
            man_score += score
        elif value[0] == 'BRONX':
            bx_count += 1
            if value[1] == 'A':
                score = float(GRADES.get('A'))
            elif value[1] == 'B':
                score = float(GRADES.get('B'))
            elif value[1] == 'C':
                score = float(GRADES.get('C'))
            elif value[1] == 'D':
                score = float(GRADES.get('D'))
            elif value[1] == 'F':
                score = float(GRADES.get('F'))
            bx_score += score
        elif value[0] == 'STATEN ISLAND':
            si_count += 1
            if value[1] == 'A':
                score = float(GRADES.get('A'))
            elif value[1] == 'B':
                score = float(GRADES.get('B'))
            elif value[1] == 'C':
                score = float(GRADES.get('C'))
            elif value[1] == 'D':
                score = float(GRADES.get('D'))
            elif value[1] == 'F':
                score = float(GRADES.get('F'))
            si_score += score

    score_summary = {
        'MANHATTAN': (man_count, man_score / man_count),
        'QUEENS': (qns_count, qns_score / qns_count),
        'BROOKLYN': (bkl_count, bkl_score / bkl_count),
        'BRONX': (bx_count, bx_score / bx_count),
        'STATEN ISLAND': (si_count, si_score / si_count),
        }
    return score_summary


def get_market_density(file_name=''):
    """computes market density. json usage

    Args:
        file_name (str): input file

    Returns:
        m_dict (dic): market data

    Example:
        >>> get_market_density('green_markets.json')
        {u'STATEN ISLAND': 2, u'BROOKLYN': 48, u'BRONX': 32,
        u'MANHATTAN': 39, u'QUEENS': 16}
    """

    fhandler = json.load(open(file_name, 'r'))
    data = fhandler['data']

    m_dict = {}

    for item in data:
        item[8] = item[8].strip()
        if item[8] not in m_dict.iterkeys():
            val = 1
        else:
            val = m_dict[item[8]] + 1
        m_dict[item[8]] = val
        m_dict.update(m_dict)
    return m_dict


def correlate_data(file1='', file2='', output=''):
    """tie the data together and write to file

    Args:
        file1 (str): csv input file
        file2 (str): json input file
        output (str): file to create and write to

    Returns:
        output to file

    Example:
       >>>def correlate_data('inspection_results.csv',
                                                           'green_boroughs.json',
                                                           'correlate.json')
       {'BRONX': (0.9762820512820514, 0.1987179487179487)}
    """

    score_info = get_score_summary(file1)
    market_info = get_market_density(file2)

    corr_dict = {}

    for key, value in score_info.iteritems():
        corr_dict[key] = (value[1], float(market_info[key])/float(value[0]))

    with open(output, 'w') as out:
        json.dump(corr_dict, out)
    out.close()

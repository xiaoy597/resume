# -*- coding:utf-8 -*-

import smtplib
import re
import codecs

black_words = {
    'text_filter_word': [
        '大专',
        '非统招',
        '职业学院',
        '职业技术学院',
        '专修学院',
        '商务学院',
        '教育学院',
        '思源学院',
        '经济学院',
        '金融学院',
        '中医学院',
        '北京卓达经济管理研修学院',
        '长春理工大学光电信息学院',
        '河北大学工商学院',
        '曲阜远东学院',
        '江西中医药大学',
        '黑龙江工程学院',
        '黄淮学院',
        '哈工大华德学院',
        '北京电影学院',

    ],

    'subject_filter_word': [
        '项目经理',
        '女士',
        '先生',
    ],

    'pattern_list': [
        r'1994年\d+月',
        r'1995年\d+月',
        r'1996年\d+月',
        r'1997年\d+月',
        r'22\s*岁',
        r'21\s*岁',
        r'20\s*岁',
        r'23\s*岁',
        r'1年工作经验',
        r'学院\s+英语',
        r'学院\s+(国际)?金融',
        r'学院\s+(工商)?管理',
        r'学院\s+法学',
        r'学院\s+广播影视编导',
        r'学院\s+其他',
        r'学院\s+会计',
        r'学院\s+旅游',
        r'学院\s+生物',
        r'学院\s+农学',
    ]
}

white_words = {
    'text_filter_word': [
        '大学英语六级',
    ],

    'subject_filter_word': [
    ],

    'pattern_list': [
    ]
}

first_class_colleges = []


def get_college_list():
    for line in codecs.open(r'c:\tmp\college.txt', encoding='gbk'):
        fields = line.split('\t')
        first_class_colleges.append(fields[1].encode('utf8'))

def filter_row(row, conditions):

    fields = row.split('","')
    for word in conditions['subject_filter_word']:
        if fields[0].find(word.decode('utf8')) >= 0:
            return False

    for word in conditions['text_filter_word']:
        if fields[1].find(word.decode('utf8')) >= 0:
            return False

    for pattern in conditions['pattern_list']:
        if re.search(pattern.decode('utf8'), fields[1]) is not None:
            return False

    return True


def select_row(row):
    return not filter_row(row, white_words)


def leave_row(row):
    return filter_row(row, black_words)


def process_row(row):
    fields = row.split('","')
    print fields[0], fields[2]
    # print '>>>>>>>>>>>>>>>>>>\n' + fields[1] + '\n'


def process_resumes():
    f = codecs.open(r'c:\tmp\resumes.csv', 'r', 'gbk')
    row = ''
    rows = []
    garbage_input = False
    print f.readline()

    while True:
        try:
            line = f.readline()
        except UnicodeDecodeError:
            print 'Found garbage row'
            garbage_input = True
            continue

        if not line:
            if not garbage_input:
                rows.append(row)
            break

        line = line.strip()

        if line.startswith(r'"(Zhaopin.com)') or line.startswith(r'"(51job.com)'):
            if not garbage_input and len(row) > 0:
                rows.append(row)
            garbage_input = False
            row = line
        else:
            row = row + line

    print 'Number of rows is %d\n' % len(rows)

    filtered_rows = filter(leave_row, rows)

    print 'Number of filtered rows %d\n' % len(filtered_rows)

    if len(first_class_colleges) == 0:
        get_college_list()

    white_words['text_filter_word'].extend(first_class_colleges)

    favoured_rows = filter(select_row, filtered_rows)

    print '\nFavoured resumes:'
    for row in favoured_rows:
        process_row(row)

    print '\nOther resumes:'
    for row in filtered_rows:
        process_row(row)

if __name__ == '__main__':
    process_resumes()

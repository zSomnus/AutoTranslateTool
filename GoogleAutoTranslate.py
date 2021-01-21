from googletrans import Translator
import os
import csv
from csv import writer
import sys
import time
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi


SPECIAL_CASES = {
    'ee': 'et',
}

LANGUAGES = {
    'af': 'afrikaans',
    'sq': 'albanian',
    'am': 'amharic',
    'ar': 'arabic',
    'hy': 'armenian',
    'az': 'azerbaijani',
    'eu': 'basque',
    'be': 'belarusian',
    'bn': 'bengali',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'ceb': 'cebuano',
    'ny': 'chichewa',
    'zh-cn': 'chinese (simplified)',
    'zh-tw': 'chinese (traditional)',
    'co': 'corsican',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'eo': 'esperanto',
    'et': 'estonian',
    'tl': 'filipino',
    'fi': 'finnish',
    'fr': 'french',
    'fy': 'frisian',
    'gl': 'galician',
    'ka': 'georgian',
    'de': 'german',
    'el': 'greek',
    'gu': 'gujarati',
    'ht': 'haitian creole',
    'ha': 'hausa',
    'haw': 'hawaiian',
    'iw': 'hebrew',
    'he': 'hebrew',
    'hi': 'hindi',
    'hmn': 'hmong',
    'hu': 'hungarian',
    'is': 'icelandic',
    'ig': 'igbo',
    'id': 'indonesian',
    'ga': 'irish',
    'it': 'italian',
    'ja': 'japanese',
    'jw': 'javanese',
    'kn': 'kannada',
    'kk': 'kazakh',
    'km': 'khmer',
    'ko': 'korean',
    'ku': 'kurdish (kurmanji)',
    'ky': 'kyrgyz',
    'lo': 'lao',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'lb': 'luxembourgish',
    'mk': 'macedonian',
    'mg': 'malagasy',
    'ms': 'malay',
    'ml': 'malayalam',
    'mt': 'maltese',
    'mi': 'maori',
    'mr': 'marathi',
    'mn': 'mongolian',
    'my': 'myanmar (burmese)',
    'ne': 'nepali',
    'no': 'norwegian',
    'or': 'odia',
    'ps': 'pashto',
    'fa': 'persian',
    'pl': 'polish',
    'pt': 'portuguese',
    'pa': 'punjabi',
    'ro': 'romanian',
    'ru': 'russian',
    'sm': 'samoan',
    'gd': 'scots gaelic',
    'sr': 'serbian',
    'st': 'sesotho',
    'sn': 'shona',
    'sd': 'sindhi',
    'si': 'sinhala',
    'sk': 'slovak',
    'sl': 'slovenian',
    'so': 'somali',
    'es': 'spanish',
    'su': 'sundanese',
    'sw': 'swahili',
    'sv': 'swedish',
    'tg': 'tajik',
    'ta': 'tamil',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'ug': 'uyghur',
    'uz': 'uzbek',
    'vi': 'vietnamese',
    'cy': 'welsh',
    'xh': 'xhosa',
    'yi': 'yiddish',
    'yo': 'yoruba',
    'zu': 'zulu',
}


class MainWindow(QDialog):
    lang_list = [
        'Afrikaans',
        'Albanian',
        'Amharic',
        'Arabic',
        'Armenian',
        'Azerbaijani',
        'Basque',
        'Belarusian',
        'Bengali',
        'Bosnian',
        'Bulgarian',
        'Catalan',
        'Cebuano',
        'Chichewa',
        'Chinese (simplified)',
        'Chinese (traditional)',
        'Corsican',
        'Croatian',
        'Czech',
        'Danish',
        'Dutch',
        'English',
        'Esperanto',
        'Estonian',
        'Filipino',
        'Finnish',
        'French',
        'Frisian',
        'Galician',
        'Georgian',
        'German',
        'Greek',
        'Gujarati',
        'Haitian creole',
        'Hausa',
        'Hawaiian',
        'Hebrew',
        'Hebrew',
        'Hindi',
        'Hmong',
        'Hungarian',
        'Icelandic',
        'Igbo',
        'Indonesian',
        'Irish',
        'Italian',
        'Japanese',
        'Javanese',
        'Kannada',
        'Kazakh',
        'Khmer',
        'Korean',
        'Kurdish (kurmanji)',
        'Kyrgyz',
        'Lao',
        'Latin',
        'Latvian',
        'Lithuanian',
        'Luxembourgish',
        'Macedonian',
        'Malagasy',
        'Malay',
        'Malayalam',
        'Maltese',
        'Maori',
        'Marathi',
        'Mongolian',
        'Myanmar (burmese)',
        'Nepali',
        'Norwegian',
        'Odia',
        'Pashto',
        'Persian',
        'Polish',
        'Portuguese',
        'Punjabi',
        'Romanian',
        'Russian',
        'Samoan',
        'Scots gaelic',
        'Serbian',
        'Sesotho',
        'Shona',
        'Sindhi',
        'Sinhala',
        'Slovak',
        'Slovenian',
        'Somali',
        'Spanish',
        'Sundanese',
        'Swahili',
        'Swedish',
        'Tajik',
        'Tamil',
        'Telugu',
        'Thai',
        'Turkish',
        'Ukrainian',
        'Urdu',
        'Uyghur',
        'Uzbek',
        'Vietnamese',
        'Welsh',
        'Xhosa',
        'Yiddish',
        'Yoruba',
        'Zulu',
    ]

    lang_key_list = [
        'af',
        'sq',
        'am',
        'ar',
        'hy',
        'az',
        'eu',
        'be',
        'bn',
        'bs',
        'bg',
        'ca',
        'ceb',
        'ny',
        'zh-cn',
        'zh-tw',
        'co',
        'hr',
        'cs',
        'da',
        'nl',
        'en',
        'eo',
        'et',
        'tl',
        'fi',
        'fr',
        'fy',
        'gl',
        'ka',
        'de',
        'el',
        'gu',
        'ht',
        'ha',
        'haw',
        'iw',
        'he',
        'hi',
        'hmn',
        'hu',
        'is',
        'ig',
        'id',
        'ga',
        'it',
        'ja',
        'jw',
        'kn',
        'kk',
        'km',
        'ko',
        'ku',
        'ky',
        'lo',
        'la',
        'lv',
        'lt',
        'lb',
        'mk',
        'mg',
        'ms',
        'ml',
        'mt',
        'mi',
        'mr',
        'mn',
        'my',
        'ne',
        'no',
        'or',
        'ps',
        'fa',
        'pl',
        'pt',
        'pa',
        'ro',
        'ru',
        'sm',
        'gd',
        'sr',
        'st',
        'sn',
        'sd',
        'si',
        'sk',
        'sl',
        'so',
        'es',
        'su',
        'sw',
        'sv',
        'tg',
        'ta',
        'te',
        'th',
        'tr',
        'uk',
        'ur',
        'ug',
        'uz',
        'vi',
        'cy',
        'xh',
        'yi',
        'yo',
        'zu',
    ]

    lang_index = 0
    read_from = ''
    write_to = ''

    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("main.ui", self)

        self.browseFile.clicked.connect(self.browsefiles)
        self.browseDirectory.clicked.connect(self.browseDirectories)
        self.trans_lang.addItems(self.lang_list)
        self.translate.clicked.connect(self.translation)

    def browsefiles(self):
        fname = QFileDialog.getOpenFileName(
            self, "Open file", 'D:\\', 'TSV files (*.tsv)')
        self.filename.setText(fname[0])
        self.read_from = self.filename.text()

    def browseDirectories(self):
        dname = QFileDialog.getExistingDirectory(self, 'D:\\')
        self.directoryname.setText(dname)
        self.write_to = self.directoryname.text()

    def translation(self):
        original_language = 'en'
        translate_language = self.lang_key_list[self.lang_index]
        target_row = 5

        tr = Translator()
        tr.raise_Exception = True

        # Read .tsv file
        read_from_path = self.read_from
        with open(read_from_path, 'rt', encoding='utf8') as f:
            reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
            column = [row[target_row] for row in reader]

        # Write to file
        path = self.write_to + original_language + '_' + \
            translate_language + '_' + 'translation.tsv'

        with open(path, 'w', newline="", encoding='utf8') as f:
            csv_write = csv.writer(f)
            count = 0
            for content in column:
                if content:
                    csv_write.writerow(
                        [tr.translate(content, src=original_language, dest=translate_language).text])
                    count += 1
                    time.sleep(0.5)
                else:
                    csv_write.writerow('')
                    count += 1
                print(str(count) + "/" + str(len(column)))

        f.close()


app = QApplication(sys.argv)
mainWindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainWindow)
widget.setFixedWidth(400)
widget.setFixedHeight(300)
widget.show()
sys.exit(app.exec_())

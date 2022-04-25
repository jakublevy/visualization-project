from argparse import ArgumentParser
import json
import matplotlib.pyplot as plt
import mplcursors

words = None
kanji = None

index = []
occ = []

f_kanji = None
f_word = None

num_2_uta = {}

def main():
    ap = ArgumentParser()
    add_args(ap)
    args = ap.parse_args()
    load_kanji()
    load_words()
    build_index()
    for t in args.text:
        plot(args.kanji, t)


def load_kanji():
    global kanji, kanji_l
    with open('../data/poem-kanji.json') as f:
        kanji = json.load(f)
        kanji_l = list(kanji)


def load_words():
    global words, words_l
    with open('../data/poem-words.json') as f:
        words = json.load(f)
        words_l = list(words)


def build_index():
    global index
    for p_num in kanji:
        index.append(p_num)
        num_2_uta[p_num] = kanji[p_num]['name']


def plot(kanji, findtxt):
    if kanji:
        plot_kanji(findtxt)
    else:
        plot_words(findtxt)


def plot_kanji(find_kanji):
    global f_kanji
    f_kanji = find_kanji
    for p_num in kanji:
        if find_kanji in kanji[p_num]:
            occ.append(kanji[p_num][find_kanji])
        else:
            occ.append(0)

    plt.rcParams['font.family'] = 'Meiryo'
    fig, ax = plt.subplots()
    lines = ax.plot(index, occ, 'o')
    ax.set_title(f'Kanji {find_kanji}')
    ax.set_xlabel('Uta Number')
    ax.set_ylabel('Occurrences')
    ax.set_xticks([0,499,999,1499,1999,2499,2999,3499,3999,4499])
    ax.set_yticks(list(range(0,max(occ)+1, 1)))
    c = mplcursors.cursor(lines, hover=True)
    c.connect('add', kanji_formatter)
    plt.show()


def kanji_formatter(v):
    idx = int(v.target[0])
    k = kanji_l[idx]
    occ = 0
    if f_kanji in kanji[str(k)]:
        occ = int(kanji[str(k)][f_kanji])
    w = ''
    if occ > 0:
        kk = words[str(k)][f_kanji].keys()
        vv = []
        for ke in kk:
            vv.append(f'{ke} {words[str(k)][f_kanji][ke]}')
        w = '\n'.join(vv)
    c = num_2_uta[k]
    if w == '':
        v.annotation.set(text=f'歌 {c}\n# {occ}', ma='left', fontsize=16)
    else:
        v.annotation.set(text=f'歌 {c}\n# {occ}\n{w}', ma='left', fontsize=16)


def word_formatter(v):
    idx = int(v.target[0])
    k = kanji_l[idx]
    occ = 0
    ww = words[str(k)].values()
    li = None
    for item in ww:
        if f_word in item:
            li = item
    if li is not None:
        occ = li[f_word]
    v.annotation.set(text=f'歌 {k}\n# {occ}', ma='left', fontsize=16)


def plot_words(findtxt):
    global f_word
    f_word = findtxt
    for p_num in words:
        items = words[p_num].values()
        for ii in items:
            if findtxt in ii:
                occ.append(ii[findtxt])
                break
        else:
            occ.append(0)

    plt.rcParams['font.family'] = 'Meiryo'
    fig, ax = plt.subplots()
    lines = ax.plot(index, occ, 'o')
    ax.set_title(f'Word {findtxt}')
    ax.set_xlabel('Uta Number')
    ax.set_ylabel('Occurrences')
    ax.set_xticks([0,500,1000,1499,1999, 2500, 2999+13, 3499+35,3999+45, 4500+44])
    ax.set_yticks(list(range(0,max(occ)+1, 1)))
    c = mplcursors.cursor(lines, hover=True)
    c.connect('add', word_formatter)
    plt.show()


def add_args(ap):
    ap.add_argument('text', nargs='*', type=str, help='Text or kanji to plot heatmap of')

    ap.add_argument('-k', '--kanji', action='store_true', help='Treat the input text as kanji (default: %(default)s)')


if __name__ == '__main__':
    main()

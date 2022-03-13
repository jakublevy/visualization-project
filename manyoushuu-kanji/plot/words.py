import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from wordcloud import WordCloud

words = {}
kanji_info = {}

def main():
    global words, kanji_info

    with open('../words.json') as f:
        tmp_wordsForKanji = json.load(f)
        for k in tmp_wordsForKanji:
            for w in tmp_wordsForKanji[k]:
                words[w] = tmp_wordsForKanji[k][w]

    with open('kanji-info.json') as f:
        kanji_info = json.load(f)

    wordcloud = WordCloud(max_words=200, width = 2000, height = 1500, prefer_horizontal=1.0, color_func=color, background_color='white', font_path='C:\\Windows\\Fonts\\meiryo.ttc').generate_from_frequencies(words)
    fig, ax = plt.subplots()
    plt.rcParams['font.family'] = 'Meiryo'
    other = mpatches.Patch(color='#c0c0c0', label='Other')
    n1 = mpatches.Patch(color='#ef5350', label='JLPT N1')
    n2 = mpatches.Patch(color='#ffa726', label='JLPT N2')
    n3 = mpatches.Patch(color='#D9B611', label='JLPT N3')
    n4 = mpatches.Patch(color='#9ccc65', label='JLPT N4')
    n5 = mpatches.Patch(color='#26a69a', label='JLPT N5')
    ax.legend(handles=[other,n1,n2,n3,n4,n5], loc='upper right', bbox_to_anchor=(1.1,1))
    ax.axis('off')
    ax.imshow(wordcloud)
    plt.tight_layout(pad=0)
    plt.show()


def color(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    req_lvl = None
    for c in word:
        if c in kanji_info:
            new_lvl = kanji_info[c]['jlpt']
            if req_lvl is None or (req_lvl is not None and new_lvl < req_lvl):
                req_lvl = new_lvl
    
    if req_lvl == -1: #unclassified
        return '#c0c0c0'
    elif req_lvl == 1:
        return '#ef5350'
    elif req_lvl == 2:
        return '#ffa726'
    elif req_lvl == 3:
        return '#D9B611'
    elif req_lvl == 4:
        return '#9ccc65'
    return '#26a69a'

if __name__ == "__main__":
    main()
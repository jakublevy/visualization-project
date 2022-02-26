import json
from matplotlib import pyplot as plt
import matplotlib.font_manager as fm
import math

kanji = {}
wordsForKanji = {}
word_count = 0
kanji_pairs_sorted = []
most_freq_kanji_occ_count = 0
kanji_with_most_words = None
words_occ = {}
kanji_info = {}

def main():
    global kanji, wordsForKanji, word_count, kanji_pairs_sorted, most_freq_kanji_occ_count, kanji_with_most_words, kanji_info

    with open('../kanji.json') as f:
        kanji = json.load(f)
        kanji = {k: v for k, v in sorted(kanji.items(), key=lambda item: item[1], reverse=True)}

    with open('../words.json') as f:
        tmp_wordsForKanji = json.load(f)
        for k in tmp_wordsForKanji:
            wordsForKanji[k] = {k: v for k, v in sorted(tmp_wordsForKanji[k].items(), key=lambda item: item[1], reverse=True)}

    with open('kanji-info.json') as f:
        kanji_info = json.load(f)

    word_count = sum(kanji.values())
    most_freq_kanji_occ_count = kanji[next(iter(kanji))]
    kanji_with_most_words = max([(len(wordsForKanji[x]), x) for x in wordsForKanji],key=lambda y:y[0])[1]
    build_words_occ()
    plot_freq()
    print('ff')

def kanji_freq(kanji_symb):
    return (kanji[kanji_symb] / most_freq_kanji_occ_count) * 100

def kanji_word_freq(kanji_symb):
    return (words_occ[kanji_symb] / words_occ[kanji_with_most_words]) * 100

def build_words_occ():
    global words_occ
    for kanji in wordsForKanji:
        words_occ[kanji] = len(wordsForKanji[kanji])


class freq_obj:
    def __init__(self, x, y, kanji):
        self.x = x
        self.y = y
        self.kanji = kanji

    def pt(self):
        return (self.x,self.y)

def plot_freq():

    def on_pick(event):
        for plot_obj in to_plot:
            if event.mouseevent.xdata and event.mouseevent.ydata and pt_distance(plot_obj.pt(), (event.mouseevent.xdata,event.mouseevent.ydata)) < 1:
                print(plot_obj.kanji)
                return

    plt.rcParams['font.family'] = 'Meiryo'
    annotated = []
    fig, ax = plt.subplots()
    to_plot = []
    for k in kanji:
        to_plot.append(freq_obj(kanji_freq(k), kanji_word_freq(k), k))
    for obj in to_plot:
        ax.plot(obj.x, obj.y, 'o',picker=5, color=jlpt_color(obj.kanji))
        if not collide(obj.x, obj.y, annotated) and pt_distance((obj.x,obj.y), (0,0)) > 20:
            #https://stackoverflow.com/questions/22052532/matplotlib-python-clickable-points
            ax.annotate(obj.kanji, xy=(obj.x, obj.y), xytext=(2,3), xycoords='data', textcoords='offset points')
            annotated.append((obj.x+2,obj.y+3))

    ax.legend(['Other','JLPT N1', 'JLPT N2', 'JLPT N3', 'JLPT N4', 'JLPT N5'])
    leg = ax.get_legend()
    leg.legendHandles[0].set_color('#c0c0c0')
    leg.legendHandles[1].set_color('#ef5350')
    leg.legendHandles[2].set_color('#ffa726')
    leg.legendHandles[3].set_color('#ffee58')
    leg.legendHandles[4].set_color('#9ccc65')
    leg.legendHandles[5].set_color('#26a69a')
    ax.set_title('Frequency vs Word Count for Kanji')
    ax.set_xlabel('Frequency')
    ax.set_ylabel('Word Count')
    fig.canvas.callbacks.connect('pick_event', on_pick)
#5 25
    annot = ax.annotate("", xy=(0,0), xytext=(5,25),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"), fontsize=16)
    annot.set_visible(False)

    def update_annot(plot_obj):
        annot.set_text(plot_obj.kanji)
        
        top = kanji_info[plot_obj.kanji]['freq']
        suffix = 'th'
        if top == 1:
            suffix = 'st'
        elif top == 2:
            suffix = 'nd'
        elif top == 3:
            suffix = 'rd'

        strokes = kanji_info[plot_obj.kanji]['strokes']
        if top != -1:
            txt = f'{plot_obj.kanji} {top}{suffix}【{strokes}画】\n#O: {kanji[plot_obj.kanji]}\n#W: {words_occ[plot_obj.kanji]}'
        else:
            txt = f'{plot_obj.kanji}【{strokes}画】\n#O: {kanji[plot_obj.kanji]}\n#W: {words_occ[plot_obj.kanji]}'

        words = wordsForKanji[plot_obj.kanji]
        max = min(3, len(words))
        i = 0
        while i < max:
            txt += f'\n{list(words)[i]}: {words[list(words)[i]]}'
            i += 1
        annot.set_text(txt)
        annot.xy = plot_obj.pt()
        annot.get_bbox_patch().set_facecolor(jlpt_color(plot_obj.kanji))
        annot.get_bbox_patch().set_alpha(0.7)
        # x = 5
        # if plot_obj.x > 50:
        #     x = -5
        # y = 25
        # if plot_obj.y > 50:
        #     y = -25
        # annot.xytext = (x,y)

    def on_hover(event):
        for plot_obj in to_plot:
            if event.xdata and event.ydata and pt_distance(plot_obj.pt(), (event.xdata,event.ydata)) < 1:
                update_annot(plot_obj)
                annot.set_visible(True)
                fig.canvas.draw_idle()
                return
        annot.set_visible(False)
        fig.canvas.draw_idle()

    fig.canvas.mpl_connect("motion_notify_event", on_hover)
    plt.show()

def jlpt_color(kanji):
    color = '#c0c0c0' # other
    if kanji_info[kanji]['jlpt'] == 1:
        color = '#ef5350'
    elif kanji_info[kanji]['jlpt'] == 2:
        color = '#ffa726'
    elif kanji_info[kanji]['jlpt'] == 3:
        color = '#ffee58'
    elif kanji_info[kanji]['jlpt'] == 4:
        color = '#9ccc65'
    elif kanji_info[kanji]['jlpt'] == 5:
        color = '#26a69a'
    return color

def collide(x, y, annotated):
    pt = (x+2, y+3)
    for an_pt in annotated:
        d = pt_distance(pt, an_pt)
        if d < 1.5:
            return True
    return False

def pt_distance(pt,an_pt):
    x1 = pt[0]
    y1 = pt[1]
    x2 = an_pt[0]
    y2 = an_pt[1]
    return math.sqrt((x1-x2)*(x1-x2) + (y1-y2) * (y1-y2))

if __name__ == "__main__":
    main()
import json
from matplotlib import pyplot as plt
import mplcursors

katauta = [5,7,7]
tanka = [5,7,5,7,7]
sedouka = [5,7,7,5,7,7]
bussokusekika = [5,7,5,7,7,7]

utas = {}

types_dist = {}
types_name = {}

def main():
    global utas
    with open('../data/poem-morae.json') as f:
        utas = json.load(f)

    plot_types()

def plot_types():
    def on_hover(sel):
        i = sel.annotation._text.index('=')
        j = sel.annotation._text.index('\n')
        type = sel.annotation._text[i+1:j]
        txt = f'y={int(sel.target[1])}\n'
        if type == 'katauta':
            txt += cust_join(types_name['katauta'], 20)
        elif type == 'tanka':
            txt += cust_join(types_name['tanka'], 20)
        elif type == 'sedouka':
            txt += cust_join(types_name['sedouka'], 20)
        elif type == 'chouka':
            txt += cust_join(types_name['chouka'], 20)
        elif type == 'bussokusekika':
            txt += cust_join(types_name['bussokusekika'], 20)
        elif type == 'indeterminate':
            txt += cust_join(types_name['indeterminate'], 20)
        sel.annotation.set(text=txt, ma='left')


    utas_l = list(utas.items())

    types_dist['katauta'] = 0
    types_dist['indeterminate'] = 0
    types_dist['tanka'] = 0
    types_dist['chouka'] = 0
    types_dist['sedouka'] = 0
    types_dist['bussokusekika'] = 0

    types_name['katauta'] = []
    types_name['indeterminate'] = []
    types_name['tanka'] = []
    types_name['chouka'] = []
    types_name['sedouka'] = []
    types_name['bussokusekika'] = []

    for i in range(0, len(utas_l)):
        k = utas_l[i][0]
        v = utas_l[i][1]
        d = determine_poem(v['morae'])
        types_dist[d] += 1
        types_name[d].append(utas_l[i][1]['name'])
    
    plt.rcParams['font.family'] = 'Meiryo'
    fig, ax = plt.subplots()

    types = list(types_dist.keys())
    values = list(types_dist.values())
    lines = ax.bar(types, values, width=0.3)

    ax.set_title('Uta Types')
    ax.set_ylabel('#Uta')
    cursor = mplcursors.cursor(hover=True)
    cursor.connect('add', on_hover)
    plt.show()

def cust_join(data, n):
    txt = ''
    for i in range(len(data)):
        if i > 1 and (i-1)%n == 0:
            txt += data[i] + '\n'
        else:
            txt += data[i] + ', '
    txt = txt[:-1]
    if txt[-1] == ',':
        txt = txt[:-1]
    return txt

def determine_poem(morae):
    if len(morae) == 3:
        return 'katauta'
        # h = l1_dist(haiku, morae)
        # if h == 0:
        #     return 'haiku'
        # k = l1_dist(katauta, morae)
        # if k < h:
        #     return 'haiku'
        # elif k > h:
        #     return 'katauta'
        # return 'indeterminate'
    if len(morae) == 5:
        return 'tanka'
    if len(morae) == 6:
        s = l1_dist(sedouka, morae)
        if s == 0:
            return 'sedouka'
        b = l1_dist(bussokusekika, morae)
        if s < b:
            return 'sedouka'
        if s > b:
            return 'bussokusekika'
        return 'indeterminate'
    elif len(morae) >= 7:
        return 'chouka'

    return 'indeterminate'
    #raise Exception(f'Invalid morae {morae}')

def l1_dist(x, y):
    assert len(x) == len(y)
    d = 0
    for i in range(len(x)):
        d += abs(x[i] - y[i])

    return d
    
if __name__ == '__main__':
    main()
import json
from matplotlib import pyplot as plt
from matplotlib.backend_bases import MouseButton
import pyperclip
import math


utas = {}
pool = None

katauta = [5,7,7]
tanka = [5,7,5,7,7]
sedouka = [5,7,7,5,7,7]
bussokusekika = [5,7,5,7,7,7]

ANNOTATE_SHIFT_X = 20
ANNOTATE_SHIFT_Y = 25

chouka_3221_3346 = 0
# CPU_COUNT = 6

def main():
    global utas, pool #, CPU_COUNT
    with open('../data/poem-morae.json') as f:
        utas = json.load(f)

    # CPU_COUNT = multiprocessing.cpu_count()
    # pool = multiprocessing.Pool(CPU_COUNT)
    plot_freq()

def plot_freq():
    global chouka_3221_3346
    def on_mousepress(event):
         if event.button in [MouseButton.LEFT, MouseButton.RIGHT]:
            if event.xdata is None or event.ydata is None:
                return
            closest = to_plot[0]
            closest_dist = pt_distance(to_plot[0].pt(), (event.xdata, event.ydata))
            for i in range(1, len(to_plot)):
                d = pt_distance((event.xdata, event.ydata), to_plot[i].pt()) 
                if d < closest_dist:
                    closest = to_plot[i]
                    closest_dist = d
            if closest_dist < 30:
                if event.button is MouseButton.LEFT:
                    pyperclip.copy(closest.y)
                elif event.button is MouseButton.RIGHT:
                    pyperclip.copy(annot_txt(closest))

    plt.rcParams['font.family'] = 'Meiryo'
    fig, ax = plt.subplots()
    to_plot = []
    utas_l = list(utas.items())
    for i in range(0, len(utas_l)):
        k = utas_l[i][0]
        v = utas_l[i][1]
        t = determine_poem(v['morae'])
        to_plot.append(freq_obj(i, v['poemCount'], utas_l[i][1]['name'], v['morae'], t))
        if t == 'chouka' and (',' in utas_l[i][1]['name'] or (int(utas_l[i][1]['name']) >= 3221 and int(utas_l[i][1]['name']) <= 3346)):
            chouka_3221_3346 += 1
    for obj in to_plot:
        ax.plot(obj.x, obj.y, 'o',picker=5)

    ax.set_title('歌と節数')
    ax.set_xlabel('Uta Number')
    ax.set_ylabel('Number of Verse')
    ax.set_xticks([0,500,1000,1500,2000,2500,3000,3500,4000,4500])
    fig.canvas.callbacks.connect('button_press_event', on_mousepress)
#5 25
    annot = ax.annotate("", xy=(0,0), xytext=(ANNOTATE_SHIFT_X,ANNOTATE_SHIFT_Y),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"), fontsize=16, va='top')
    annot.set_visible(False)

    def update_annot(plot_obj):        
        annot.set_text(annot_txt(plot_obj))
        annot.xy = plot_obj.pt()
        annot.get_bbox_patch().set_facecolor('#ef5350')
        annot.get_bbox_patch().set_alpha(0.7)

    def annot_txt(plot_obj):
        txt = f'歌：{plot_obj.name}\n'
        txt += f'{plot_obj.type}\n'
        txt += f'節の数: {plot_obj.y}\n'
        m = ', '.join(map(str, plot_obj.morae))
        txt += f'モーラ: {m}'
        return txt

    def on_hover(event):
        if event.xdata is None or event.ydata is None:
            annot.set_visible(False)
            fig.canvas.draw_idle()
            return
        closest = to_plot[0]
        closest_dist = pt_distance(to_plot[0].pt(), (event.xdata, event.ydata))
        for i in range(1, len(to_plot)):
            d = pt_distance((event.xdata, event.ydata), to_plot[i].pt()) 
            if d < closest_dist:
                closest = to_plot[i]
                closest_dist = d
        if closest_dist < 30:
            update_annot(closest)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            annot.set_visible(False)
            fig.canvas.draw_idle()

    fig.canvas.mpl_connect("motion_notify_event", on_hover)
    plt.show()

        # if event.xdata is None or event.ydata is None:
        #     return 
        # event_pt = (event.xdata, event.ydata)
        # l = len(to_plot)
        # d = math.ceil(l/CPU_COUNT)
        # mapped = []
        # for i in range(CPU_COUNT):
        #     if (i+1)*d > l:
        #         mapped.append(to_plot[i*d:])    
        #     else:
        #         mapped.append(to_plot[i*d:(i+1)*d])
            
        # g = partial(find_closest, event_pt=event_pt)
        # dists =pool.map(g, mapped)
        # sm_dist = dists[0]
        # #print(sm_dist[0])
        # for i in range(1,len(dists)):
        #     if dists[i][0] < sm_dist[0]:
        #         sm_dist = dists[i]

        # if sm_dist[0] < 15:
        #     update_annot(sm_dist[1])
        #     annot.set_visible(True)
        #     fig.canvas.draw_idle()
        #     return

        # annot.set_visible(False)
        # fig.canvas.draw_idle()

        # fig.canvas.mpl_connect("motion_notify_event", on_hover)
        # plt.show()

def find_closest(plot_objs, event_pt):
        min_dist = pt_distance(plot_objs[0].pt(), event_pt)
        min_obj = plot_objs[0]
        for i in range(1, len(plot_objs)):
            newd = pt_distance(plot_objs[i].pt(), event_pt)
            if newd < min_dist:
                min_dist = newd
                min_obj = plot_objs[i]
        return (min_dist, min_obj)



def collide(x, y, annotated):
    pt = (x+2, y+5)
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
    
class freq_obj:
    def __init__(self, x, y, name, morae, type):
        self.x = x
        self.y = y
        self.name = name
        self.morae = morae
        self.type = type

    def pt(self):
        return (self.x,self.y)

if __name__ == '__main__':
    main()
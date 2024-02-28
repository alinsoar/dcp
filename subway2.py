
def subway(**lines):
    """Define a subway map. Input is subway(linename='station1 station2...'...).
    Convert that and return a dict of the form: {station:{neighbor:line,...},...}"""
    ## your code here
    dic = {}
    limits = []
    for color, stationlist in lines.items():
        sl = stationlist.split(':')
        limits += [sl[0], sl[-1]]
        l1 = [None] + sl[:-1]
        l2 = sl[1:] + [None]
        for s,n in filter(None, sum([[(s,nl) if nl else nl,(s,nr) if nr else nr]
                                     for s,nl,nr in zip(sl,l1,l2)], [])):
            d = dic.get(s, None)
            if d: d[n] = color
            else: dic [s] = {n: color}
    return dic,limits

boston,lboston = subway(
    blue='bowdoin:government:state:aquarium:maverick:airport:suffolk:revere:wonderland',
    orange='oakgrove:sullivan:haymarket:state:downtown:chinatown:tufts:backbay:foresthills',
    green='lechmere:science:north:haymarket:government:park:copley:kenmore:newton:riverside',
    red='alewife:davis:porter:harvard:central:mit:charles:park:downtown:south:umass:mattapan')

from paris_metro import line1, line2, line3, line3b, line4, line5, line6, line7, line7b, line8, line9, line10, line11, line12, line13, line14
paris,lparis = subway (
    line1 = line1,
    line2 = line2,
    line3 = line3,
    line3b = line3b,
    line4 = line4,
    line5 = line5,
    line6 = line6,
    line7 = line7,
    line7b = line7b,
    line8 = line8,
    line9 = line9,
    line10 = line10,
    line11 = line11,
    line12 = line12,
    line13 = line13,
    line14 = line14
)

parisstattions = sorted([x for x in paris])

def ride(here, there, system):
    "Return a path on the subway system from here to there."
    #print here, '->', there
    explored = set()
    queue = [[here]]
    while queue:
        path = queue.pop(0)
        last = path[-1]
        for (nextstation, color) in system[last].items():
            #if nextstation in path: continue
            if nextstation not in explored:
                explored.add (nextstation)
                p2 = path + [color, nextstation]
                if nextstation == there: return p2
                queue.append (p2);

def longest_ride(system, l):
    """"Return the longest possible 'shortest path' 
    ride between any two stops in the system."""
    ## your code here
    res = []
    for t in l:
        for s in l:
            if s!=t:
                path = ride(s,t, system)
                res.append (path)
    return sorted(res, key = lambda x : len(x), reverse = True)[0]
    # print l
    # return sorted( [ride(s,t, system)
    #                 for t in l
    #                 for s in l
    #                 if s!=t],
    #                key = lambda x : len(x), reverse = True)[0]

def ride_paris (fromstation, tostation):
    return ride(parisstattions[fromstation], parisstattions[tostation], paris)

#########################################################################################


# print paris stations by index -- difficult to call by name, instead of index
for i,x in enumerate(parisstattions): print '%d\t%s' % (i, x)

def print_path(path, msg):
    print
    print "--------------------", msg
    lines = path [1::2]
    stations = path[0::2]
    for x in zip(lines, stations): print x

#shortest path between 2 metro stations in Paris
# call by index
print_path (ride_paris(194, 201), "**")

#shortest path between 2 metro stations in Boston - Massachusetts
#call by name
#print  ride ('mit', 'state', boston)

print_path ( longest_ride (paris, lparis), "+++") # breadth first blocks

# longest 
print longest_ride (boston, lboston)



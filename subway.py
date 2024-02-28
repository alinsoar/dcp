# -----------------
# User Instructions
# 
# Write a function, subway, that takes lines as input (read more about
# the **lines notation in the instructor comments box below) and returns
# a dictionary of the form {station:{neighbor:line, ...}, ... } 
#
# For example, when calling subway(boston), one of the entries in the 
# resulting dictionary should be 'foresthills': {'backbay': 'orange'}. 
# This means that foresthills only has one neighbor ('backbay') and 
# that neighbor is on the orange line. Other stations have more neighbors:
# 'state', for example, has 4 neighbors.
#
# Once you've defined your subway function, you can define a ride and 
# longest_ride function. ride(here, there, system) takes as input 
# a starting station (here), a destination station (there), and a subway
# system and returns the shortest path.
#
# longest_ride(system) returns the longest possible ride in a given 
# subway system. 

# -------------
# Grading Notes
#
# The subway() function will not be tested directly, only ride() and 
# longest_ride() will be explicitly tested. If your code passes the 
# assert statements in test_ride(), it should be marked correct.

def subway(**lines):
    """Define a subway map. Input is subway(linename='station1 station2...'...).
    Convert that and return a dict of the form: {station:{neighbor:line,...},...}"""
    ## your code here
    dic = {}
    for color, stationlist in lines.items():
        sl = stationlist.split(':')
        l1 = [None] + sl[:-1]
        l2 = sl[1:] + [None]
        for s,n in filter(None, sum([[(s,nl) if nl else nl,(s,nr) if nr else nr]
                                     for s,nl,nr in zip(sl,l1,l2)], [])):
            d = dic.get(s, None)
            if d: d[n] = color
            else: dic [s] = {n: color}
    #for x in dic.items(): print x
    return dic

boston = subway(
    blue='bowdoin:government:state:aquarium:maverick:airport:suffolk:revere:wonderland',
    orange='oakgrove:sullivan:haymarket:state:downtown:chinatown:tufts:backbay:foresthills',
    green='lechmere:science:north:haymarket:government:park:copley:kenmore:newton:riverside',
    red='alewife:davis:porter:harvard:central:mit:charles:park:downtown:south:umass:mattapan')

from paris_metro import line1, line2, line3, line3b, line4, line5, line6, line7, line7b, line8, line9, line10, line11, line12, line13, line14
paris = subway (
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

def ride(here, there, system=boston):
    "Return a path on the subway system from here to there."
    def okay (state): return okay is there
    def successors(station): return system[station].items()
    # print here, '->', there
    explored = set()
    queue = [[here]]
    while queue:
        path = queue.pop(0)
        last = path[-1]
        if last == there: return path
        for (nextstation, color) in successors(last):
            p2 = path + [color, nextstation]
            pz = frozenset (p2)
            if pz not in explored:
                explored.add (pz)
                queue.append (p2);

def longest_ride(system):
    """"Return the longest possible 'shortest path' 
    ride between any two stops in the system."""
    ## your code here
    return sorted( [ride(s,t, system)
                    for t in system
                    for s in system
                    if s!=t],
                   key = lambda x : len(x), reverse = True)[0]

def shortest_path_search(start, successors, is_goal):
    """Find the shortest path from start state to a state
    such that is_goal(state) is true."""
    if is_goal(start):
        return [start]
    explored = set() # set of states we have visited
    frontier = [ [start] ] # ordered list of paths we have blazed
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        for (state, action) in successors(s).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if is_goal(state):
                    return path2
                else:
                    frontier.append(path2)
    return []

def path_states(path):
    "Return a list of states in this path."
    return path[0::2]
    
def path_actions(path):
    "Return a list of actions in this path."
    return path[1::2]

def test_ride():
    assert ride('mit', 'government') == [ 'mit', 'red', 'charles', 'red', 'park', 'green', 'government']

    assert ride('mattapan', 'foresthills') == [
        'mattapan', 'red', 'umass', 'red', 'south', 'red', 'downtown',
        'orange', 'chinatown', 'orange', 'tufts', 'orange', 'backbay', 'orange', 'foresthills']

    assert ride('newton', 'alewife') == [
        'newton', 'green', 'kenmore', 'green', 'copley', 'green', 'park', 'red', 'charles', 'red',
        'mit', 'red', 'central', 'red', 'harvard', 'red', 'porter', 'red', 'davis', 'red', 'alewife']

    assert (path_states(longest_ride(boston)) == [
        'wonderland', 'revere', 'suffolk', 'airport', 'maverick', 'aquarium', 'state', 'downtown', 'park',
        'charles', 'mit', 'central', 'harvard', 'porter', 'davis', 'alewife'] or 
        path_states(longest_ride(boston)) == [
                'alewife', 'davis', 'porter', 'harvard', 'central', 'mit', 'charles', 
                'park', 'downtown', 'state', 'aquarium', 'maverick', 'airport', 'suffolk', 'revere', 'wonderland'])

    assert len(path_states(longest_ride(boston))) == 16

    return 'test_ride passes'

print test_ride()

def rideboston()

def rideparis (here, there, system=boston):

for x in enumerate(paris): print x




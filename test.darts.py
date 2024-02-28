
sectors = ('20', '1', '18', '4', '13', '6', '10', '15', '2', '17', '3',
        '19', '7', '16', '8', '11', '14', '9', '12', '5')    


ring = "5 20 1 18 4 13 6 10 15 2 17 3 19 7 16 8 11 14 9 12 5 20".split()
neighbour = dict ([(ring[i], (ring[i-1], ring[i+1]))
                   for i in range (1, len(ring)-1)])
neighbour = dict ({'B': tuple(set(ring)), 'OFF': tuple(set(ring)) },
                  **neighbour )

targets = ["D" + x for x in ring[1:-1]] + ["S" + x for x in ring[1:-1]] + ["T" + x for x in ring[1:-1]] + ['SB', 'DB']

def ring_outcome(target, miss):
    t = target[0]
    D = ((t, 1-miss),)
    R = ((('S', miss),) if t == 'T' else
         (('S', 2*miss/3), ('SB', miss/3)) if target == 'DB' else
         (('S', miss/2), ('OFF', miss/2)) if t == 'D' else
         (('S', 3*miss/4), ('DB', miss/4)) if target == 'SB' else
         (('D', miss/2), ('T', miss/2))) #if t == 'S' 
    return dict(D+R)

def sector_outcome(target, miss):
    n = target[1:] if target != 'OFF' else target
    K = neighbour[n]
    return dict ([(n, 1-miss)] + [(k, miss/len(K)) for k in K])


def SB_outcome(miss):
    radial_probs = {'S': 3.0 * miss / 4.0, 'SB': 1.0 - miss, 'DB': miss / 4.0}
    cross_probs = {'S': miss, 'B': 1.0 - miss}

    cell_probs = dict([[rl + cl, rp * cp]
                       for (rl, rp) in radial_probs.items()
                       for (cl, cp) in cross_probs.items()])

    S_sum = 0.0
    outcome = {}
    for label, cell_prob in cell_probs.items():
        if label == 'DBB':
            outcome['DB'] = cell_prob
        elif label == 'SBB':
            outcome['SB'] = cell_prob
        else:
            S_sum += cell_prob
    sector_share = S_sum / 20.0
    for sector in sectors:
        outcome['S' + sector] = sector_share
    return outcome

def DB_outcome(miss):
    miss_3 = 1.0 - ((1.0 - miss) / 3.0)

    radial_probs = {'S': miss_3 / 3.0, 'SB': 2.0 * miss_3 / 3.0, 'DB': 1.0 - miss_3}
    cell_probs = dict([[r_label + c_label, r_prob * c_prob]
            for (r_label, r_prob) in radial_probs.items()
            for (c_label, c_prob) in radial_probs.items()])

    S_sum = 0.0
    SB_sum = 0.0
    outcome = {}
    for label, cell_prob in cell_probs.items():
        if label == 'DBDB':
            outcome['DB'] = cell_prob
        elif label == 'SBDB' or label == 'DBSB':
            SB_sum += cell_prob
        else:
            S_sum += cell_prob
    outcome['DB'] = SB_sum
    sector_share = S_sum / 20.0
    for sector in sectors:
        outcome['S' + sector] = sector_share
    return outcome

def outcome(target, miss):
    "Cell probability distribution."
    if target == 'SB':
        return SB_outcome(miss)
    elif target == 'DB':
        return DB_outcome(miss)
    else:
        ring_probs = ring_outcome(target, miss)
        sector_probs = sector_outcome(target, miss)
        print ring_probs
        print sector_probs
        return dict([[ring + sector, r_prob * s_prob]
                     for (ring, r_prob) in ring_probs.items()
                     for (sector, s_prob) in sector_probs.items()])
print outcome('S7', 0.6)

exit(0)

def target_score(target):
    if target[:3] == 'OFF':
        return 0
    if target == 'SB':
        return 25
    if target == 'DB':
        return 50
    ring = target[0]
    sector = target[1:]
    score = int(sector)
    if ring == 'D':
        score *= 2
    elif ring == 'T':
        score *= 3
    return score

def expected_score(target, miss):
    cell_probs = outcome(target, miss)
    total = 0.0
    for target, prob in cell_probs.items():
        total += prob * target_score(target)
    return total

def best_target(miss):
    "Return the target that maximizes the expected score for one dart."
    best_score = -999
    best_target = None
    for target in targets:
        score = expected_score(target, miss)
        print target, miss, '\t\t', score
        if score > best_score:
            best_score = score
            best_target = target
    return best_target

print best_target(0.6)

def same_outcome(dict1, dict2):
    "Two states are the same if all corresponding sets of locs are the same."
    return all(abs(dict1.get(key, 0) - dict2.get(key, 0)) <= 0.0001
               for key in set(dict1) | set(dict2))

def test_darts2():
    assert best_target(0.0) == 'T20'
    assert best_target(0.1) == 'T20'
    assert best_target(0.4) == 'T19'
    assert same_outcome(outcome('T20', 0.0), {'T20': 1.0})
    assert same_outcome(
        outcome('T20', 0.1), 
        {'T20': 0.81, 'S1': 0.005, 'T5': 0.045, 
         'S5': 0.005, 'T1': 0.045, 'S20': 0.09})
    assert (same_outcome(
        outcome('SB', 0.2),
        {'S9': 0.016, 'S8': 0.016, 'S3': 0.016, 'S2': 0.016, 'S1': 0.016,
         'DB': 0.04, 'S6': 0.016, 'S5': 0.016, 'S4': 0.016,
         'S20': 0.016,
         'S19': 0.016, 'S18': 0.016, 'S13': 0.016, 'S12': 0.016,
         'S11': 0.016,
         'S10': 0.016, 'S17': 0.016, 'S16': 0.016, 'S15': 0.016,
         'S14': 0.016,
         'S7': 0.016, 'SB': 0.64}))
test_darts2()

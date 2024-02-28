
rings = ['OFF', 'D', 'S', 'T', 'SB', 'DB']
ring_index = {'OFF': 0, 'D': 1, 'DB': 5, 'S': 2, 'T': 3, 'SB': 4}

sectors = ('20', '1', '18', '4', '13', '6', '10', '15', '2', '17', '3',
        '19', '7', '16', '8', '11', '14', '9', '12', '5')    
sector_index = {'11': 15, '10': 6, '13': 4, '12': 18, '20': 0, '14': 16,
        '17': 9, '16': 13, '19': 11, '18': 2, '1': 1, '3': 10, '2': 8,
        '5': 19, '4': 3, '7': 12, '6': 5, '9': 17, '15': 7, '8': 14}

targets = ['D20', 'D1', 'D18', 'D4', 'D13', 'D6', 'D10', 'D15', 'D2',
        'D17', 'D3', 'D19', 'D7', 'D16', 'D8', 'D11', 'D14', 'D9', 'D12',
        'D5', 'S20', 'S1', 'S18', 'S4', 'S13', 'S6', 'S10', 'S15', 'S2',
        'S17', 'S3', 'S19', 'S7', 'S16', 'S8', 'S11', 'S14', 'S9', 'S12',
        'S5', 'T20', 'T1', 'T18', 'T4', 'T13', 'T6', 'T10', 'T15', 'T2',
        'T17', 'T3', 'T19', 'T7', 'T16', 'T8', 'T11', 'T14', 'T9', 'T12', 'T5',
        'SB', 'DB']

def ring_outcome(target, miss):                                       # OFF?
    "Radial probability distribution, outside the bulls."
    # (Darts targeted for the single ring (S) may hit D or T
    # but never the bulls (SB and DB).)
    ring = target[0]
    if ring == 'D':
        return {'OFF': miss / 2.0, 'D': 1.0 - miss, 'S': miss / 2.0}
    if ring == 'S':
        miss = miss / 5.0
        return {'D': miss / 2.0, 'S': 1.0 - miss, 'T': miss / 2.0}
    if ring == 'T':
        return {'S': miss, 'T': 1.0 - miss}
    raise ValueError('Illegal target/ring.')

def sector_outcome(target, miss):                                       # OFF?
    "Circumferential probability distribution, outside the bulls."
    sector = target[1:]
    if sector not in sector_index:
            raise ValueError('Illegal target/sector.')
    i = sector_index[sector]
    return {sectors[(i - 1) % 20]: miss / 2.0,
            sector: 1.0 - miss,
            sectors[(i + 1) % 20]: miss / 2.0}

def SB_outcome(miss):
    # 'B' refers to probability mass along the original centerline,
    # as opposed to those misses that move into S along the cross axis.
    radial_probs = {'S': 3.0 * miss / 4.0, 'SB': 1.0 - miss, 'DB': miss / 4.0}
    cross_probs = {'S': miss, 'B': 1.0 - miss}

    # Form the cross-product.
    cell_probs = dict([[r_label + c_label, r_prob * c_prob]
            for (r_label, r_prob) in radial_probs.items()
            for (c_label, c_prob) in cross_probs.items()])

    # Redistribute the single-ring (S) probability mass.
    # (Difficult to justify except as a large ensemble statistic.)
    # (The SB result should actually be much, much higher.
    # DBS should all go to DB instead of S, as should most of SBS.)
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
    # 'B' refers to probability mass along the original centerline,
    # as opposed to those misses that move into S along the cross axis.

    # "Triple" the miss rate by dividing the hit rate by 3.
    miss_3 = 1.0 - ((1.0 - miss) / 3.0)

    # Use radial symmetry: only one set of probabilities needed.
    # (Or were we given the over-all probabilities, and have
    # no need to compute a cross-product?)
    radial_probs = {'S': miss_3 / 3.0, 'SB': 2.0 * miss_3 / 3.0, 'DB': 1.0 - miss_3}
    cell_probs = dict([[r_label + c_label, r_prob * c_prob]
            for (r_label, r_prob) in radial_probs.items()
            for (c_label, c_prob) in radial_probs.items()])

    # Redistribute the single-ring (S) probability mass.
    # (The SB result should actually be somewhat higher.)
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
    else:                                                     # Sum the OFF#?
        ring_probs = ring_outcome(target, miss)
        sector_probs = sector_outcome(target, miss)
        return dict([[ring + sector, r_prob * s_prob]
            for (ring, r_prob) in ring_probs.items()
            for (sector, s_prob) in sector_probs.items()])

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
    # Assumes that 'OFF' (or 'OFF#') cannot be the answer.
    best_score = -999
    best_target = None
    for target in targets:
        score = expected_score(target, miss)
        if score > best_score:
            best_score = score
            best_target = target
    return best_target



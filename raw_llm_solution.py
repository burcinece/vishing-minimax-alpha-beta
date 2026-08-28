import copy

ATTACKER_ACTIONS = {
    'A1': {'risk': 10, 'trust': 0, 'pressure': 20},
    'A2': {'risk': 12, 'trust': 10, 'pressure': 10},
    'A3': {'risk': 5, 'trust': 20, 'pressure': 0},
    'A4': {'risk': 15, 'trust': -5, 'pressure': 25},
    'A5': {'risk': 10, 'trust': 15, 'pressure': 5},
    'A6': {'risk': 25, 'trust': -10, 'pressure': 10},
    'A7': {'risk': 30, 'trust': -15, 'pressure': 15},
    'A8': {'risk': 15, 'trust': 15, 'pressure': 10},
}

DEFENDER_ACTIONS = {
    'D1': {'risk': 0, 'trust': 0, 'cost': 0},
    'D2': {'risk': -10, 'trust': -5, 'cost': 2},
    'D3': {'risk': -20, 'trust': -10, 'cost': 5},
    'D4': {'risk': -30, 'trust': -15, 'cost': 8},
    'D5': {'risk': -40, 'trust': -25, 'cost': 12},
}

def baslangic_durumu():
    return {
        'turn': 0,
        'risk_score': 0,
        'trust_level': 50,
        'pressure_level': 0,
        'disclosed_info': 0,
        'verification_status': 0,
        'conversation_status': 'devam',
    }

def saldirgan_uygula(durum, eylem):
    yeni = copy.deepcopy(durum)
    etki = ATTACKER_ACTIONS[eylem]
    yeni['risk_score'] = min(100, yeni['risk_score'] + etki['risk'])
    yeni['trust_level'] = yeni['trust_level'] + etki['trust']
    yeni['pressure_level'] = max(0, min(100, yeni['pressure_level'] + etki['pressure']))
    if eylem in ('A6', 'A7'):
        yeni['disclosed_info'] = min(3, yeni['disclosed_info'] + 1)
    yeni['turn'] += 1
    return yeni

def savunucu_uygula(durum, eylem):
    yeni = copy.deepcopy(durum)
    etki = DEFENDER_ACTIONS[eylem]
    yeni['risk_score'] = max(0, yeni['risk_score'] + etki['risk'])
    yeni['trust_level'] = yeni['trust_level'] + etki['trust']
    if eylem == 'D3':
        yeni['verification_status'] = 1
    if eylem == 'D4':
        yeni['conversation_status'] = 'engellendi'
    if eylem == 'D5':
        yeni['conversation_status'] = 'sonlandirildi'
    yeni['turn'] += 1
    return yeni

def terminal_kontrol(durum):
    if durum['risk_score'] >= 100:
        return True, -100
    if durum['disclosed_info'] >= 3 and durum['verification_status'] == 0:
        return True, -100
    if durum['conversation_status'] == 'engellendi':
        return True, 70
    if durum['verification_status'] == 1:
        return True, 80
    if durum['conversation_status'] == 'sonlandirildi':
        if durum['risk_score'] >= 40:
            return True, 90
        return True, -30
    if durum['turn'] >= 6:
        return True, None
    return False, None

def heuristik(durum):
    deger = 0.0
    deger -= durum['risk_score'] * 1.0
    deger += durum['verification_status'] * 40
    deger -= durum['disclosed_info'] * 5
    deger -= durum['pressure_level'] * 0.3
    deger += durum['trust_level'] * 0.1
    return deger

dugum_sayaci = 0

def minimax(durum, derinlik, max_oyuncu):
    global dugum_sayaci
    dugum_sayaci += 1
    bitti, deger = terminal_kontrol(durum)
    if bitti:
        return (deger if deger is not None else heuristik(durum)), None
    if derinlik == 0:
        return heuristik(durum), None
    if max_oyuncu:
        en_iyi_deger = float('-inf')
        en_iyi_eylem = None
        for eylem in DEFENDER_ACTIONS:
            cocuk = savunucu_uygula(durum, eylem)
            deger, _ = minimax(cocuk, derinlik - 1, False)
            if deger > en_iyi_deger:
                en_iyi_deger = deger
                en_iyi_eylem = eylem
        return en_iyi_deger, en_iyi_eylem
    else:
        en_iyi_deger = float('inf')
        en_iyi_eylem = None
        for eylem in ATTACKER_ACTIONS:
            cocuk = saldirgan_uygula(durum, eylem)
            deger, _ = minimax(cocuk, derinlik - 1, True)
            if deger < en_iyi_deger:
                en_iyi_deger = deger
                en_iyi_eylem = eylem
        return en_iyi_deger, en_iyi_eylem

def alpha_beta(durum, derinlik, alpha, beta, max_oyuncu):
    global dugum_sayaci
    dugum_sayaci += 1
    bitti, deger = terminal_kontrol(durum)
    if bitti:
        return (deger if deger is not None else heuristik(durum)), None
    if derinlik == 0:
        return heuristik(durum), None
    if max_oyuncu:
        en_iyi_deger = float('-inf')
        en_iyi_eylem = None
        for eylem in DEFENDER_ACTIONS:
            cocuk = savunucu_uygula(durum, eylem)
            deger, _ = alpha_beta(cocuk, derinlik - 1, alpha, beta, False)
            if deger > en_iyi_deger:
                en_iyi_deger = deger
                en_iyi_eylem = eylem
            alpha = max(alpha, en_iyi_deger)
            if beta <= alpha:
                break
        return en_iyi_deger, en_iyi_eylem
    else:
        en_iyi_deger = float('inf')
        en_iyi_eylem = None
        for eylem in ATTACKER_ACTIONS:
            cocuk = saldirgan_uygula(durum, eylem)
            deger, _ = alpha_beta(cocuk, derinlik - 1, alpha, beta, True)
            if deger < en_iyi_deger:
                en_iyi_deger = deger
                en_iyi_eylem = eylem
            beta = min(beta, en_iyi_deger)
            if beta <= alpha:
                break
        return en_iyi_deger, en_iyi_eylem

if __name__ == '__main__':
    baslangic = baslangic_durumu()
    deger, eylem = alpha_beta(baslangic, 4, float('-inf'), float('inf'), True)
    print(f"Kok dugum en iyi eylem: {eylem}  deger: {deger}")
    print(f"Ziyaret edilen dugum sayisi: {dugum_sayaci}")

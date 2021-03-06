import flask
import json
import math
import numpy as np
from uuid import uuid1
from datetime import datetime

# stolen from CardUtil.js
expByLvl = [0, 110, 250, 430, 660, 950, 1310, 1750, 2280, 2910, 3640, 4470, 5400, 6430, 7560, 8790, 10120, 11550, 13080, 14710, 16440, 18270, 20200, 22230, 24360, 26590, 28920, 31350, 33880, 36510, 39240, 42070, 45E3, 48030, 51160, 54390, 57720, 61150, 64680, 68310, 72040, 75870, 79800, 83830, 87960, 92190, 96520, 100950, 105480, 110110, 114840, 119670, 124600, 129630, 134760, 139990, 145320, 150750, 156280, 161910, 167640, 173470, 179400, 185430, 191560, 197790, 204120, 210550, 217080, 223710, 230440, 237270, 244200, 251230, 258360, 265590, 272920, 280350, 287880, 295510,
        303240, 311070, 319E3, 327030, 335160, 343390, 351720, 360150, 368680, 377310, 386040, 394870, 403800, 412830, 421960, 431190, 440520, 449950, 459480, 469110
    ]
itemExp = [100, 500, 2500]
rankNumbers = {
    'RANK_1': 1,
    'RANK_2': 2,
    'RANK_3': 3,
    'RANK_4': 4,
    'RANK_5': 5
}
maxLevels = {
    'RANK_1': 40,
    'RANK_2': 50,
    'RANK_3': 60,
    'RANK_4': 80,
    'RANK_5': 100
}
extraCCByRank = {
    'RANK_1': 1,
    'RANK_2': 2,
    'RANK_3': 3
}
baseCCByRank = {
    'RANK_1': 5,
    'RANK_2': 50,
    'RANK_3': 400
}

with open('data/user/user.json', encoding='utf-8') as f:
    userInfo = json.load(f)
userId = userInfo['id']

def getCCAmount(rank, level, useItem):
    totalCC = 0
    if rank in rankNumbers:
        levelExtraCC, baseCC, rankMult = [rankNumbers[rank]]*3
    else:
        levelExtraCC, baseCC, rankMult = [0]*3

    for itemId, amount in useItem.items():
        itemRank = itemId.split("_")[-1]
        if itemRank == "PP":
            itemRank = "RANK_3"
        elif itemRank == "P":
            itemRank = "RANK_2"
        else:
            itemRank = "RANK_1"

        baseCC = baseCCByRank[itemRank]
        levelExtraCC = extraCCByRank[itemRank]
        totalCC += math.floor((baseCC + (level - 1) * levelExtraCC) * rankMult) * amount
    return totalCC

def calculateMultiplier(rank, level):
    rank1Mults = [0, .05, .1, .15, .2, .25, .3, .35, .41, .46, .51, .56, .61, .66, .71, .76, .82, .87, .92, .97, 1.02, 1.07, 1.12, 1.17, 1.23, 1.28, 1.33, 1.38, 1.43, 1.48, 1.53, 1.58, 1.64, 1.69, 1.74, 1.79, 1.84, 1.89, 1.94, 2]
    rank2Mults = [0, .04, .08, .13, .17, .22, .26, .31, .35, .4, .44, .49, .53, .58, .62, .67, .71, .76, .8, .85, .89, .94, .98, 1.03, 1.07, 1.12, 1.16, 1.21, 1.25, 1.3, 1.34, 1.39, 1.43, 1.48, 1.52, 1.57, 1.61, 1.66, 1.7, 1.75, 
                    1.79, 1.84, 1.88, 1.93, 1.97, 2.02, 2.06, 2.11, 2.15, 2.2]
    rank3Mults = [0, .04, .08, .12, .16, .2, .24, .28, .32, .36, .4, .44, .48, .52, .56, .61, .65, .69, .73, .77, .81, .85, .89, .93, .97, 1.01, 1.05, 1.09, 1.13, 1.17, 1.22, 1.26, 1.3, 1.34, 1.38, 1.42, 1.46, 1.5, 1.54, 1.58, 
                    1.62, 1.66, 1.7, 1.74, 1.78, 1.83, 1.87, 1.91, 1.95, 1.99, 2.03, 2.07, 2.11, 2.15, 2.19, 2.23, 2.27, 2.31, 2.35, 2.4]
    rank4Mults = [0, .03, .06, .09, .13, .16, .19, .23, .26, .29, .32, .36, .39, .42, .46, .49, .52, .55, .59, .62, .65, .69, .72, .75, .78, .82, .85, .88, .92, .95, .98, 1.02, 1.05, 1.08, 1.11, 1.15, 1.18, 1.21, 1.25, 1.28, 1.31, 
                    1.34, 1.38, 1.41, 1.44, 1.48, 1.51, 1.54, 1.57, 1.61, 1.64, 1.67, 1.71, 1.74, 1.77, 1.81, 1.84, 1.87, 1.9, 1.94, 1.97, 2, 2.04, 2.07, 2.1, 2.13, 2.17, 2.2, 2.23, 2.27, 2.3, 2.33, 2.36, 2.4, 2.43, 2.46, 2.5, 
                    2.53, 2.56, 2.6]
    rank5Mults = [0, .03, .06, .09, .12, .15, .18, .21, .24, .27, .3, .33, .36, .39, .42, .45, .48, .51, .54, .57, .6, .63, .66, .69, .72, .75, .78, .81, .84, .87, .9, .93, .96, 1, 1.03, 1.06, 1.09, 1.12, 1.15, 1.18, 1.21, 1.24, 
                    1.27, 1.3, 1.33, 1.36, 1.39, 1.42, 1.45, 1.48, 1.51, 1.54, 1.57, 1.6, 1.63, 1.66, 1.69, 1.72, 1.75, 1.78, 1.81, 1.84, 1.87, 1.9, 1.93, 1.96, 2, 2.03, 2.06, 2.09, 2.12, 2.15, 2.18, 2.21, 2.24, 2.27, 2.3, 2.33, 
                    2.36, 2.39, 2.42, 2.45, 2.48, 2.51, 2.54, 2.57, 2.6, 2.63, 2.66, 2.69, 2.72, 2.75, 2.78, 2.81, 2.84, 2.87, 2.9, 2.93, 2.96, 3]
    if rank == "RANK_1":
        return rank1Mults[level - 1]
    if rank == "RANK_2":
        return rank2Mults[level - 1]
    if rank =="RANK_3":
        return rank3Mults[level - 1]
    if rank == "RANK_4":
        return rank4Mults[level - 1]
    if rank == "RANK_5":
        return rank5Mults[level - 1]
    return 1

# stolen from CardUtil.js
def getStats(baseCard, rank, level):
    growthType = baseCard['growthType']

    if level > maxLevels[rank]: level = maxLevels[rank]

    stats = {
        'attack': baseCard['attack'],
        'defense': baseCard['defense'],
        'hp': baseCard['hp']
    }

    multipliers = {
        'BALANCE': [1,1,1],
        'ATTACK': [1.03, 0.97, 0.98],
        'DEFENSE': [0.98, 1.05, 0.97],
        'HP': [0.97, 0.98, 1.04],
        'ATKDEF': [1.02, 1.01, 0.99],
        'ATKHP': [1.01, 0.99, 1.02],
        'DEFHP': [0.99, 1.02, 1.01]
    }

    level = calculateMultiplier(rank, level)
    atkMult, defMult, hpMult = multipliers[growthType]
    multDict = {'attack': atkMult, 'defense': defMult, 'hp': hpMult}
            
    for key in ['attack', 'defense', 'hp']:
        stats[key] = math.ceil(baseCard[key] + baseCard[key] * level * multDict[key])
    return stats

def getComposeExp(cardElem, items):
    exp = 0
    for itemId, amount in items.items():
        isSameElement = 1.5 if cardElem in itemId or 'ALL' in itemId else 1

        addExp = itemExp[0]
        if '_PP' in itemId:
            addExp = itemExp[2]
        elif '_P' in itemId:
            addExp = itemExp[1]
        
        exp += addExp * isSameElement * amount

    return exp

def spend(items):
    # items is a list of (itemId, amount)
    with open('data/user/userItemList.json', encoding='utf-8') as f:
        itemList = json.load(f)
    
    revisedItemList = []
    for i in range(len(itemList)):
        for itemId, amount in items.items():
            if amount < 0:
                raise ValueError('Tried to spend a negative amount of mats >:(')
            if itemId == itemList[i]['itemId']:
                itemList[i]['quantity'] -= amount
                if itemList[i]['quantity'] < 0:
                    raise ValueError('Tried to spend more mats than they have D:')
                revisedItemList.append(itemList[i])

    with open('data/user/userItemList.json', 'w+', encoding='utf-8') as f:
        json.dump(itemList, f, ensure_ascii=False)

    return revisedItemList

def spendGift(gifts):
    # gifts is a list of (giftId, amount)
    with open('data/user/userGiftList.json', encoding='utf-8') as f:
        giftList = json.load(f)
    
    revisedGiftList = []
    for i in range(len(giftList)):
        for giftId, giftNum in gifts.items():
            if giftNum < 0:
                raise ValueError('Tried to spend a negative amount of mats >:(')
                return
            if giftId == giftList[i]['giftId']:
                giftList[i]['quantity'] -= giftNum
                if giftList[i]['quantity'] < 0:
                    raise ValueError('Tried to spend more mats than they have D:')
                    return
                revisedGiftList.append(giftList[i])

    with open('data/user/userGiftList.json', 'w+', encoding='utf-8') as f:
        json.dump(giftList, f, ensure_ascii=False)

    return giftList

def setUserCard(cardId, args):
    with open('data/user/userCardList.json', encoding='utf-8') as f:
        userCardList = json.load(f)
        
    for i in range(len(userCardList)):
        if userCardList[i]['id'] == cardId and userCardList[i]['enabled']:
            for arg in args.keys():
                userCardList[i][arg] = args[arg]
        
    with open('data/user/userCardList.json', 'w+', encoding='utf-8') as f:
        json.dump(userCardList, f, ensure_ascii=False)

def getFinalLevel(targetUserCard, exp):
    origLevel = targetUserCard['level']
    finalExp = expByLvl[origLevel-1] + targetUserCard['experience'] + exp
    newLevel = 1
    extraExp = 0
    for i in range(len(expByLvl)-1, 0, -1): # maybe implement a binary rather than a linear search?
        if expByLvl[i] <= finalExp:
            newLevel = i+1
            extraExp = finalExp - expByLvl[i]
            break
    return newLevel, extraExp

def compose():
    body = flask.request.json
    targetUserCardId = body['userCardId']

    with open('data/user/userCardList.json', encoding='utf-8') as f:
        userCardList = json.load(f)
    
    targetUserCard = {}
    for userCard in userCardList:
        if userCard['id'] == targetUserCardId and userCard['enabled']:
            targetUserCard = userCard
    
    if targetUserCard == {}:
        flask.abort(400, description='Tried to level up a card you don\'t have...')
        return
    
    # figure out success type
    # (totally BS rates but whatevs)
    success = np.random.choice([1, 1.5, 2], p=[0.9, 0.08, 0.02])

    # modify meguca's level and stats
    rank = targetUserCard['card']['rank']
    exp = getComposeExp(targetUserCard['card']['attributeId'], body['useItem']) * success
    newLevel, extraExp = getFinalLevel(targetUserCard, exp)

    if newLevel == maxLevels[rank]:
        extraExp = 0
    
    stats = getStats(targetUserCard['card'], rank, newLevel)
    origLevel = targetUserCard['level']
    stats['level'] = newLevel
    stats['experience'] = extraExp

    for key in stats.keys():
        targetUserCard[key] = stats[key]

    setUserCard(targetUserCardId, stats)

    # spend items
    try:
        revisedItemList = spend(body['useItem'])
    except ValueError as e:
        flask.abort(400, description='{"errorTxt": "'+repr(e)+'","resultCode": "error","title": "Error"}')

    # modify CC
    cc = getCCAmount(rank, origLevel, body['useItem'])
    with open('data/user/gameUser.json', encoding='utf-8') as f:
        gameUser = json.load(f)
    gameUser['riche'] -= cc
    if gameUser['riche'] < 0:
        flask.abort(400, description='{"errorTxt": "Tried to use more cc than you have...","resultCode": "error","title": "Error"}')
    
    with open('data/user/gameUser.json', 'w+', encoding='utf-8') as f:
        json.dump(gameUser, f, ensure_ascii=False)
    
    # make response
    response = {
        'composeEffect': success,
        'resultCode': 'success',
        'gameUser': gameUser,
        'userCardList': [targetUserCard],
        'userItemList': revisedItemList
    }
    return flask.jsonify(response)

def customize():
    body = flask.request.json
    targetUserCardId = body['userCardId']

    with open('data/user/userCardList.json', encoding='utf-8') as f:
        userCardList = json.load(f)
    
    targetUserCard = {}
    for userCard in userCardList:
        if userCard['id'] == targetUserCardId:
            targetUserCard = userCard
    
    if targetUserCard == {}:
        flask.abort(400, description='Tried to add a mat to a card you don\'t have...')
        return

    targetMatPos = body['target']

    # set info about chara
    targetUserCard['customized'+str(targetMatPos)] = True
    cardInfo = {'customized'+str(targetMatPos): True}
    setUserCard(targetUserCardId, cardInfo)

    # spend mats
    matId = targetUserCard['card']['cardCustomize']['giftId'+str(targetMatPos)]
    amount = targetUserCard['card']['cardCustomize']['giftNum'+str(targetMatPos)]
    
    try:
        revisedItemList = spendGift({matId: amount})
    except ValueError as e:
        flask.abort(400, description='{"errorTxt": "'+repr(e)+'","resultCode": "error","title": "Error"}')
    
    # make response
    response = {
        'resultCode': 'success',
        'userCardList': [targetUserCard],
        'userGiftList': revisedItemList
    }
    return flask.jsonify(response)

def evolve():
    body = flask.request.json
    targetUserCardId = body['userCardId']

    with open('data/user/userCardList.json', encoding='utf-8') as f:
        userCardList = json.load(f)
    
    targetUserCard = {}
    userCardIdx = 0
    for i in range(len(userCardList)):
        userCard = userCardList[i]
        if userCard['id'] == targetUserCardId and userCard['enabled']:
            targetUserCard = userCard
            userCardIdx = i
    
    if targetUserCard == {}:
        flask.abort(400, description='Tried to awaken a card you don\'t have...')

    # get next card
    with open('data/cards.json', encoding='utf-8') as f:
        allCharas = json.load(f)

    cardList = None
    for chara in allCharas:
        if chara['charaId'] == targetUserCard['card']['charaNo']:
            cardList = chara['cardList']
    if targetUserCard is None:
        flask.abort(400, description='Tried to awaken a character that doesn\'t exist...')
    
    newCard = None
    foundCurrentCard = False
    for card in cardList:
        if foundCurrentCard:
            newCard = card['card']
            break
        if targetUserCard['card']['cardId'] == card['cardId']:
            foundCurrentCard = True
    if newCard is None and foundCurrentCard:
        newCard = cardList[-1]['card']
    if newCard is None:
        flask.abort(400, description='This character can\'t be awakened anymore...')
    
    # make new userCard and userChara
    nowstr = str(datetime.now()).split('.')[0].replace('-', '/')
    newUserCardId = str(uuid1())
    newUserCard = {
        "id": newUserCardId,
        "userId": userId,
        "cardId": newCard['cardId'],
        "displayCardId": newCard['cardId'],
        "revision": targetUserCard['revision'],
        "attack": newCard['attack'],
        "defense": newCard['defense'],
        "hp": newCard['hp'],
        "level": 1,
        "experience": 0,
        "magiaLevel": targetUserCard['magiaLevel'],
        "enabled": True,
        "customized1": False,
        "customized2": False,
        "customized3": False,
        "customized4": False,
        "customized5": False,
        "customized6": False,
        "createdAt": nowstr,
        "card": newCard
    }
    targetUserCard['enabled'] = False
    userCardList[userCardIdx] = targetUserCard

    with open('data/user/userCharaList.json', encoding='utf-8') as f:
        userCharaList = json.load(f)
    revisedUserChara = None
    for i in range(len(userCharaList)):
        if userCharaList[i]['charaId'] == targetUserCard['card']['charaNo']:
            userCharaList[i]['userCardId'] = newUserCardId
            userCharaList[i]['card'] = newCard
            revisedUserChara = userCharaList[i]

    if revisedUserChara is None:
        flask.abort(400, description='Tried to awaken a character you don\'t have...')

    # save user info
    userCardList.append(newUserCard)
    userCardList[i]['enabled'] = False
    with open('data/user/userCardList.json', 'w+', encoding='utf-8') as f:
        json.dump(userCardList, f, ensure_ascii=False)

    with open('data/user/userCharaList.json', 'w+', encoding='utf-8') as f:
        json.dump(userCharaList, f, ensure_ascii=False)

    # spend CC
    ccByLevel = {'RANK_2': 10000, 'RANK_3': 100000, 'RANK_4': 300000, 'RANK_5': 1000000} # not sure about how much CC it takes to go from 2* to 3*
    with open('data/user/gameUser.json', encoding='utf-8') as f:
        gameUser = json.load(f)
    gameUser['riche'] -= ccByLevel[newCard['rank']]
    if gameUser['riche'] < 0:
        flask.abort(400, description='{"errorTxt": "Tried to use more cc than you have...","resultCode": "error","title": "Error"}')
    
    with open('data/user/gameUser.json', 'w+', encoding='utf-8') as f:
        json.dump(gameUser, f, ensure_ascii=False)

    # make response
    response = {
        'evolution': {
            'current': {
                'attr': targetUserCard['card']['attributeId'],
                'cardId': targetUserCard['card']['cardId'],
                'rarity': targetUserCard['card']['rank'][-1]
            },
            'giftIdList': [targetUserCard['card']['cardCustomize'][giftKey] for giftKey in targetUserCard['card']['cardCustomize'].keys() if giftKey.startswith('giftId')],
            'result': {
                'attr': newCard['attributeId'],
                'cardId': newCard['cardId'],
                'rarity': newCard['rank'][-1]
            }
        },
        "resultCode": "success",
        'gameUser': gameUser,
        'userCardList': [targetUserCard, newUserCard],
        'userCharaList': [revisedUserChara]
    }
    return flask.jsonify(response)

def limitBreak():
    body = flask.request.json
    targetUserCardId = body['userCardId']

    # edit userCard
    with open('data/user/userCardList.json', encoding='utf-8') as f:
        userCardList = json.load(f)
    
    targetUserCard = {}
    for i in range(len(userCardList)):
        if userCardList[i]['id'] == targetUserCardId and userCardList[i]['enabled']:
            userCardList[i]['revision'] += 1
            targetUserCard = userCardList[i]
    
    if targetUserCard == {}:
        flask.abort(400, description='Tried to limit break a card you don\'t have...')
    
    with open('data/user/userCardList.json', 'w+', encoding='utf-8') as f:
        json.dump(userCardList, f, ensure_ascii=False)
    
    # edit userChara
    neededGems = {'RANK_1': 10, 'RANK_2': 10, 'RANK_3': 3, 'RANK_4': 1}
    with open('data/user/userCharaList.json', encoding='utf-8') as f:
        userCharaList = json.load(f)
    
    targetUserChara = None
    for i in range(len(userCharaList)):
        if userCharaList[i]['charaId'] == targetUserCard['card']['charaNo']:
            userCharaList[i]['lbItemNum'] -= neededGems[userCharaList[i]['chara']['defaultCard']['rank']]
            targetUserChara = userCharaList[i]
    
    if targetUserChara is None:
        flask.abort(400, description='Tried to limit break a card you don\'t have...')
    
    with open('data/user/userCharaList.json', 'w+', encoding='utf-8') as f:
        json.dump(userCharaList, f, ensure_ascii=False)

    # spend cc
    ccBySlotNum = [1, 1, 1, 1] # no idea how much it actually takes lol
    with open('data/user/gameUser.json', encoding='utf-8') as f:
        gameUser = json.load(f)
    gameUser['riche'] -= ccBySlotNum[targetUserCard['revision']-1]
    if gameUser['riche'] < 0:
        flask.abort(400, description='{"errorTxt": "Tried to use more cc than you have...","resultCode": "error","title": "Error"}')
    
    with open('data/user/gameUser.json', 'w+', encoding='utf-8') as f:
        json.dump(gameUser, f, ensure_ascii=False)

    # make response
    response = {
        "resultCode": "success",
        'gameUser': gameUser,
        'userCardList': [targetUserCard],
        'userCharaList': [targetUserChara]
    }
    return flask.jsonify(response)

def composeMagia():
    body = flask.request.json
    targetUserCardId = body['userCardId']

    # change userCard magia level
    with open('data/user/userCardList.json', encoding='utf-8') as f:
        userCardList = json.load(f)
    
    targetUserCard = None
    for i in range(len(userCardList)):
        userCard = userCardList[i]
        if userCard['id'] == targetUserCardId and userCard['enabled']:
            targetUserCard = userCard
            targetUserCard['magiaLevel'] += 1
    
    if targetUserCard is None:
        flask.abort(400, description='Tried to level magia of a card you don\'t have...')

    setUserCard(targetUserCardId, {'magiaLevel': targetUserCard['magiaLevel']})

    # spend items
    giftsToSpend = {}
    magiaLevel = {2: 'first', 3: 'second', 4: 'third', 5: 'fourth'}
    magiaPrefix = magiaLevel[targetUserCard['magiaLevel']]
    with open('data/user/userCharaList.json', encoding='utf-8') as f:
        userCharaList = json.load(f)
    for chara in userCharaList:
        if chara['charaId'] == targetUserCard['card']['charaNo']:
            for i in range(6):
                if magiaPrefix+'MagiaGiftId'+str(i+1) in chara['chara'].keys() \
                and magiaPrefix+'MagiaGiftNum'+str(i+1) in chara['chara'].keys():
                    giftsToSpend[chara['chara'][magiaPrefix+'MagiaGiftId'+str(i+1)]] = chara['chara'][magiaPrefix+'MagiaGiftNum'+str(i+1)]
    
    revisedGiftList = spendGift(giftsToSpend)

    # spend CC
    ccByLevel = {2: 10000, 3: 100000, 4: 300000, 5: 1000000} # not sure about how much CC this actually takes
    with open('data/user/gameUser.json', encoding='utf-8') as f:
        gameUser = json.load(f)
    gameUser['riche'] -= ccByLevel[targetUserCard['magiaLevel']]
    if gameUser['riche'] < 0:
        flask.abort(400, description='{"errorTxt": "Tried to use more cc than you have...","resultCode": "error","title": "Error"}')
    
    with open('data/user/gameUser.json', 'w+', encoding='utf-8') as f:
        json.dump(gameUser, f, ensure_ascii=False)

    # make response
    response = {
        'resultCode': 'success',
        'gameUser': gameUser,
        'userCardList': [targetUserCard],
        'userGiftList': revisedGiftList
    }
    return flask.jsonify(response)

def handleUserCard(endpoint):
    if endpoint.endswith('compose'):
        return compose()
    elif endpoint.endswith('customize'):
        return customize()
    elif endpoint.endswith('composeMagia'):
        return composeMagia()
    elif endpoint.endswith('limitBreak'):
        return limitBreak()
    elif endpoint.endswith('evolve'):
        return evolve()
    else:
        print('userCard/'+endpoint)
        flask.abort(501, description="Not implemented")
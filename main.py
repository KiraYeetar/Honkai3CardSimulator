# -- coding: utf-8 --

import random
import pandas as pd
import matplotlib.pyplot as plt

'''
每次抽卡都会出两件物品，所以当我把两件物品的概率单独计算，模拟概率与实际概率严重不符合... ...
如果两件物品只计算了一次出货概率
模拟概率与实际概率拟合...
讲道理是真滴坑...
'''


def run():
    # 开始模拟翻车抽卡
    simulation_data = []
    for i in range(10000):
        simulation_data += [list(game_begin())]

    # 处理下数据
    simulation_data = pd.DataFrame(simulation_data, columns=['cards_count', 'is_wish_insure', 'is_weapon_insure'])

    simulation_data_tmp = simulation_data.pivot_table(index='cards_count', values='is_wish_insure', aggfunc='count').reset_index().rename(columns={'is_wish_insure': 'people_count'})
    simulation_data = pd.merge(simulation_data, simulation_data_tmp, on='cards_count', how='left')

    simulation_data_tmp = simulation_data.pivot_table(index='cards_count', values='is_wish_insure', aggfunc='sum').reset_index().rename(columns={'is_wish_insure': 'is_wish_count'})
    simulation_data = pd.merge(simulation_data, simulation_data_tmp, on='cards_count', how='left')

    simulation_data_tmp = simulation_data.pivot_table(index='cards_count', values='is_weapon_insure', aggfunc='sum').reset_index().rename(columns={'is_weapon_insure': 'is_weapon_count'})
    simulation_data = pd.merge(simulation_data, simulation_data_tmp, on='cards_count', how='left')

    del simulation_data['is_wish_insure']
    del simulation_data['is_weapon_insure']
    simulation_data = simulation_data.drop_duplicates('cards_count')

    # 人数占比（可以理解为概率）
    simulation_data = simulation_data
    people_sum = sum(simulation_data['people_count'])
    for i in range(10, 210, 10):
        print(str(i)+'抽毕业概率: '+str(sum(simulation_data[simulation_data['cards_count']<=i]['people_count'])*1.0/people_sum))

    # 开始画图
    simulation_data = simulation_data.sort_values(by='cards_count').set_index('cards_count').head(120)
    # print(simulation_data)

    plt.plot(simulation_data['people_count'], label='number of people')
    plt.plot(simulation_data['is_wish_count'], label='graduated with wishing pool')
    plt.plot(simulation_data['is_weapon_count'], label='graduated with weapon insure')
    plt.legend(loc='upper left')

    plt.xlabel('number of cards')
    plt.ylabel('number of graduation')
    plt.show()


def game_begin(mark_pro=0.0124, weapon_pro=0.02479, other_mark_pro=0.0031*12, other_weapon_pro=0.0062*4):
    mark1_up_pro = mark_pro
    mark2_up_pro = mark1_up_pro + mark_pro
    mark3_up_pro = mark2_up_pro + mark_pro
    weapon_up_pro = mark3_up_pro + weapon_pro
    other_pink_pro = weapon_up_pro+other_mark_pro+other_weapon_pro
    is_wish_insure = 0
    is_weapon_insure = 0
    # other_up_pro = 1-mark1_up_pro-mark2_up_pro-mark3_up_pro-weapon_up_pro

    god_bless_me = [0, 0, 0, 0]
    wish_pool = [0, 0, 0]
    cards_count = 0
    count_insure = 0

    while 0 in god_bless_me:
        # 先扔卡进去
        cards_count += 1
        # 得出本次概率
        one = random.uniform(0, 1)

        # 十抽保底机制
        if count_insure == 10:
            # print(str(count_all)+'抽，十连保底')
            one = random.uniform(0, other_pink_pro)

        # 武器60抽保底机制
        if (cards_count == 60) & (god_bless_me[3] == 0):
            # print('60抽，武器保底')
            one = random.uniform(mark3_up_pro, weapon_up_pro)
            is_weapon_insure = 1

        # 判断出货没有
        if one < other_pink_pro:
            count_insure = 0
            # print(str(count_all) + '抽，出货了')
            if one < mark1_up_pro:
                god_bless_me[0] += 1
                wish_pool[0] = 1
            elif one < mark2_up_pro:
                god_bless_me[1] += 1
                wish_pool[1] = 1
            elif one < mark3_up_pro:
                god_bless_me[2] += 1
                wish_pool[2] = 1
            elif one < weapon_up_pro:
                god_bless_me[3] += 1
        else:
            # 没出货就保底计数加一
            count_insure += 1

        # 许愿池机制
        if (sum(wish_pool) == 2) & (sum(god_bless_me[0:3]) >= 4):
            tmp = 2
            for j in range(3):
                if tmp == 0:
                    break
                else:
                    if god_bless_me[j] == 2:
                        god_bless_me[j] -= 1
                        tmp -= 1
                    elif god_bless_me[j] > 2:
                        god_bless_me[j] -= tmp
                        tmp = 0
            god_bless_me[wish_pool.index(0)] += 1
            wish_pool[wish_pool.index(0)] = 1
            is_wish_insure = 1
            # print('许愿池二换一 '+str(god_bless_me))

    return cards_count, is_wish_insure, is_weapon_insure


if __name__ == '__main__':
    run()

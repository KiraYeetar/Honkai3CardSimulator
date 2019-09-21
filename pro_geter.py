# -- coding: utf-8 --

import random


'''
用来计算国服非保底概率，by暴力法
结果为：单件UP圣痕概率0.30%，UP武器概率0.61%，其他四星圣痕总概率0.90%，其他四星武器总概率0.61%
误差在0.03%左右
'''


def run():
    # 开始模拟翻车抽卡
    game_begin()


def game_begin(mark_pro=0.0124, weapon_pro=0.02479, other_mark_pro=0.0031*3*4, other_weapon_pro=0.0062*4):
    mark1_up_pro = fake_mark1_up_pro = mark_pro
    mark2_up_pro = fake_mark2_up_pro = mark1_up_pro + mark_pro
    mark3_up_pro = fake_mark3_up_pro = mark2_up_pro + mark_pro
    weapon_up_pro = fake_weapon_up_pro = mark3_up_pro + weapon_pro
    other_mark_pro = fake_other_mark_pro = weapon_up_pro + other_mark_pro
    other_weapon_pro = fake_other_weapon_pro = other_mark_pro + other_weapon_pro

    stop_count = 0

    while stop_count<=20:
        pre_count = 100000
        stop_flag = 0
        # 存放上位个数，中位个数，下位个数，武器，其他圣痕，其他武器
        god_bless_me = [0, 0, 0, 0, 0, 0]
        # 保底计数
        count_insure = 0

        for index in range(pre_count):
            stop_flag = 0
            one = random.uniform(0, 0.5732)
            two = random.uniform(0.5732, 1)
            count_insure_inc = 0

            # 十抽保底机制
            if count_insure == 10:
                one = random.uniform(0, other_weapon_pro)

            for i in [one, two]:
                if i < other_weapon_pro:
                    count_insure = 0
                    if i < mark1_up_pro:
                        god_bless_me[0] += 1
                    elif i < mark2_up_pro:
                        god_bless_me[1] += 1
                    elif i < mark3_up_pro:
                        god_bless_me[2] += 1
                    elif i < weapon_up_pro:
                        god_bless_me[3] += 1
                    elif i < other_mark_pro:
                        god_bless_me[4] += 1
                    elif i < other_weapon_pro:
                        god_bless_me[5] += 1
                else:
                    count_insure_inc += 0.5

            # 本次抽卡结束， 更新多久保底
            count_insure += int(count_insure_inc)

        print(god_bless_me)

        # 0.0001的步伐更新概率. 每100000次抽卡，公示概率1.24%抽中1240±50次，以此类推所有。所有概率N次在误差内即退出循环
        if god_bless_me[0]>1290:
            mark1_up_pro -= 0.0001; stop_flag = 1
        elif god_bless_me[0]<1190:
            mark1_up_pro += 0.0001; stop_flag = 1

        if god_bless_me[1]>1290:
            mark2_up_pro -= 0.0001; stop_flag = 1
        elif god_bless_me[1]<1190:
            mark2_up_pro += 0.0001; stop_flag = 1

        if god_bless_me[2]>1290:
            mark3_up_pro -= 0.0001; stop_flag = 1
        elif god_bless_me[2]<1190:
            mark3_up_pro += 0.0001; stop_flag = 1

        if god_bless_me[3]>2530:
            weapon_up_pro -= 0.0001; stop_flag = 1
        elif god_bless_me[3]<2430:
            weapon_up_pro += 0.0001; stop_flag = 1

        if god_bless_me[4]>3770:
            other_mark_pro -= 0.0001; stop_flag = 1
        elif god_bless_me[4]<3670:
            other_mark_pro += 0.0001; stop_flag = 1

        if god_bless_me[5]>2530:
            other_weapon_pro -= 0.0001; stop_flag = 1
        elif god_bless_me[5]<2430:
            other_weapon_pro += 0.0001; stop_flag = 1

        # print(mark1_up_pro, mark2_up_pro-mark1_up_pro, mark3_up_pro-mark2_up_pro,
        #       weapon_up_pro-mark3_up_pro, other_mark_pro-weapon_up_pro, other_weapon_pro-other_mark_pro)

        if stop_flag==0:
            stop_count += 1

    print(mark1_up_pro, mark2_up_pro - mark1_up_pro, mark3_up_pro - mark2_up_pro,
          weapon_up_pro - mark3_up_pro, other_mark_pro - weapon_up_pro, other_weapon_pro - other_mark_pro)


if __name__ == '__main__':
    run()

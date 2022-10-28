#!/usr/bin/env python3

import pickle
import pprint

with open("old_articles_map.pickle", "rb") as f:
    old_maps = pickle.load(f)

pprint.pprint(old_maps)
articles_node_map = ("root", [])

branch = old_maps["our_perspectives"]


def construct_by_level(level_name, level):
    print(f"进入处理level: {level_name}")
    if len(level) > 0:
        level_payload = []
        for node_name in level:
            print(f"在<level-{level_name}>之下循环处理<node - {node_name}>")
            print(f"即将追加新的节点是({repr(node_name)}, [])")
            if isinstance(level[node_name], list):
                articles_collection = []
                if len(level[node_name]) > 0:
                    for article in level[node_name]:
                        print(f"发现一篇文章：{article}")
                        articles_collection.append(
                            (article["article_identifer"], {
                                "article_title": article["article_title"],
                                "article_excerpt": article["article_excerpt"]
                            }))
                level_payload.append(
                    (node_name.replace("粉红", "分红").replace("实时咨询", "实时资讯"),
                     articles_collection))
            elif isinstance(level[node_name], dict):
                child_level = construct_by_level(node_name, level[node_name])
                if child_level:
                    level_payload.append(child_level)
        print(f"处理level: {level_name}完毕，返回值：{level_payload}")
        return (level_name, level_payload)


articles_node_map[1].append(construct_by_level("our_perspectives", branch))

special_offer1 = ("疫情下的首选", {
    "article_title":
    "疫情下三合一 保障，100元每月起",
    "article_excerpt":
    "2020年，一场突如其来的新冠疫情夺去了很多人的生命，人们不禁感叹：活着就是幸运，存在就是坚强！时至今日，加拿大的疫情仍然没有好转的迹象，截至目前，加拿大新冠疫情确诊总数达到56.6万，死亡超过15000人。更令人担忧的是，近期在英国观察到的变异病例已在安大略省被发现。"
})

special_offer2 = ("换取AppleWatch", {
    "article_title":
    "$97换取Apple Watch 6",
    "article_excerpt":
    "Manulife Vitality是一款定期人寿保险，即在特定时间内生效的人寿保险。由加拿大最大保险公司Manulife和拥有超过2000万用户的全球健康计划领导者Vitality合作推出。此项目最适合想要坚持健身，或一直都有健身习惯的朋友。不但可以有效督促大家坚持，达成目标更能获得各种奖励。"
})

special_offer3 = ("报税省税实用妙招大揭秘", {
    "article_title":
    "2020年报税省税实用妙招大揭秘",
    "article_excerpt":
    "又到了一年报税季，很多小伙伴已经开始着手报税的准备工作。2020年受新冠疫情影响，政府推出多项紧急补贴和支援措施，纳税人在报税时需要特别留意。比如联邦政府在新冠肺炎疫情期间发放第一轮紧急救济金CERB和CESB并没有扣税，在填写2020年报税单时，就要全额申报这笔补贴金。而第二轮新冠肺炎应急措施及发放补助金CRB已扣除10%应税款额。今天小编为大家汇总了2020年报税省税妙招，供大家参考。"
})

all_special_offers = ("all_special_offers",
                      [special_offer1, special_offer2, special_offer3])
articles_node_map[1].append(all_special_offers)

pprint.pprint(articles_node_map)
"""
with open("articles_structure_map.pickle", "wb") as output_f:
    pickle.dump(articles_node_map, output_f)
"""

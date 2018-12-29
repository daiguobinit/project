# coding=gbk
import json
import ast
import re
import traceback
#
with open('./css_name.txt', 'r') as f:
# with open('./css_name_two', 'r') as f:
    contnet = f.read()
print(contnet)
contnet = contnet.replace('\n', '').replace(' ', '').replace('{', ':{')
contnet = contnet.split(';}')[:-1]
print(contnet)
# item = {}
#
# high = []
#
# for i in contnet:
#     data = str(re.search('(\d{0,5}).0px(-\d{0,5}).0px', i).group(1,2)).replace("('", '').replace("', '", '').replace("')", '')
#     data_name = i.split(':')[0].split('.')[1]
#     print(data_name, data)
#     if 'xha' in data_name:
#         num = int(str(data).split('-')[1])
#         if num not in high:
#             high.append(num)
#     data = '{"' + data + '":"' + data_name +'"}'
#     data = json.loads(data)
#     print(data)
#     item.update(data)
# print(item)
# a ='14176241311165355529'
#
# item_svg = {}
#
# # b = 7  # 1111
# # # b = 0
# # for i in range(0, len(a)):
# #     # b += 14  # 1111
# #     try:
# #         print(str(b)+'-99',":",a[i])
# #         name = str(b)+'-99'
# #         try:
# #             print(item[name])
# #             item_svg[item[name]] = str(a[i])
# #         except:
# #             pass
# #     except:
# #         pass
# #     b += 12  # 2222
# #     # b += 12
#
#
# num_list = sorted(high)
# txt_list = ['庐粘苔坝咕高侗朝戏整样桃付腿沂哈底愈芸的鸪脚孚瓣毫蒸鲜斩蛑蜜帆居', '草坡乡活孩越辣国蟾阳刘酪普庄螺慧石条划蘑粿皇剁花眉笼肺稀配醉雕糊舌', '占原养丹代扒折秘熊蝉州箱玻哺棠北松马填待钱溪尾望伏', '入蚝雅退轰顺首果麸臣乳棒拔吐络鲥可蔬肥牙字碎酱班灌木色梅藏袋鲫鸡怪窖群等馒邮豉咖锤澄板墨蛤点芋兔乾枝', '思方熠沅氽溜蕉腌冬兰芹冰糟护亭梁韭和冒随临盅蒋新七嘛蒜焚', '加绝塔鲭翅帝膏驼臊蛙书千肚蓬古乐荔恋薄多蟹宁摇滑姜锦芪拖米巴怀组犀波蓑筋卷晚鳝对瑞獐成呈萍', '简敲培狍黄髓烩吉荷绍利寿饨炖嘉妃别烘蜊飞人福葡寒罐跳唇塘', '蛇菌感鳗吃被鲁煎拆电腰苋未伦炊谢核煽捆龙砂禾营醋渠炮柳泡熘管', '健扬踏叙祥鲤茶鼋时富德烙椒登喉狮鹌门清豇菠斋肘珍府碗墙二壳浦兴琵荆裙重爽喷拌饭油塌虚野', '泥峡切头酥茸粑雪壁翡公展湘段布山饯瑚奥笋酸量极献地胭', '广干片葫潇仙啤鲻杏橙角品蛰芙莴羹南蹄佛灶爆六灸噜茗牛奶鱖盘疆牌牡御背苏藕灯霜响蓉晶排', '江敬通浇鲩村云璃鳜星烹源蜡炝罗瑰杂皋井问琉彩猫萝岛回芝煸卖口盔正鲍皮达鹑同理芦走馍贝瓤椰萄鹅珠', '圈暇熏荐譬不柱女潘为琶符鼠鲞耳血洞扇孤食保赛靖锅席阿系菊镇梭凤蚂雀乒闽平鸳肝鞭钩紫', '什鸟灼情镶孔蕨船脱温箩目臭身美枇名谭鲈母万陈煺焖盒醪婆儿番持岳狸第荪盐炸焙老汁丽抓鸯送樟佐粤参苦宜', '朱凰动铃缠球彭秋蚁炒网翘绿窝鳕姊粽信蛋鹿钟桔沛叶菱建表腐楂心柏鮰腹卤梳哩子全宋烂驴大还鹧如嫂', '雁葵开妈馓穿京浓蛎鱿满薏拼忧茭族华前浆扁西宫银鲨发鲳咬咾馄气冲栗末槟空面卦页一杞味镜仔飘扣封土丸拐熟', '蚌撕带睢丝圆年嫩丁桥浮担闸脯莉外绵筒伴官贵春宗糖虾叉聚瓶咸毛樨浸都风芽茄', '啥豌淡稚串文青绒纸生杷铁小鼻粒狼汽饼得夹猴十县鳃鹤蛏庵', '盖丰碟齿挂稿及父赠描伤长耙敦弯梨包帽润煮姬政泉黑杰阆林过郑瓯维蝤抱鸭糯东热徐菇上攒', '天做豆芜早菜莼汆狗碌须乌韩欢妹汤离焦瓜刀茉士宝意集鉴龟淮盏廖', '颜燃肴臆酿珊掌连团羲酒薯峰川两玉律斛斗胖粥众雨打告中', '鲃化杯转灵跷半拉归武力节笔鸢钵层鳞苗顾徽膳软旺樱炉巢眼脑海凉君骨块制沙锡饧', '结芫袍红捧夜庭虫根羊楚纪幔蝴件岩莲附桐柴乓把边架里法蒿托竹赤芥煨腊洪冷衣卜猪镢王榴盆叫雄', '舟粉巧围针妻肠百园邳淋施涮玫鸽香左腩铜桂池柿穗爪九屯套杆艇掐熬蒙娃霸赖喱焗', '杭喇李试苎抄易蓝钻枣吴应火合坛慈脂柔三湾延常无脆鳙荚四脊郭洋甜糕烤椿', '尖莱双饺篮远密祖跑煲拳仁单湖刺粟好指奇童列氏明象艾甘肉饽甲鹰鳖屏鳅蟠式喜虎麻环蜂蕻绣埔雾界', '茹宾陵蝶药张昌麦籽鲢叟葱鹊救五散烧汉禹廷白燕翁禧永到城八碧奉月爷陆稣麟糍田杨魔影手素亲家蕃来冻河裹', '令蟆树鬼潮神浙麒蠓苹元流水客佳金安宴夫鱼贡太鼓当翠台']
#
# for i in range(0, 28):
#     a = txt_list[i]
#     num_id = num_list[i]
#     b = 0
#     for p in range(0, len(a)):
#         # b += 14  # 1111
#         try:
#             print(str(b)+'-{}'.format(str(num_id)),":",a[p])
#             name = str(b)+'-{}'.format(str(num_id))
#             try:
#                 print(item[name])
#                 item_svg[item[name]] = str(a[p])
#             except:
#                 print(111111, traceback.format_exc())
#         except:
#             print(22222, traceback.format_exc())
#         b += 12
#
#
# print(len(contnet))
#
# print(sorted(high))
# print(len(high))
# print(item_svg)
# print(len(item_svg))
# with open('item.json', 'ab') as l:
# # with open('item_comments.json', 'ab') as l:
#     l.write(json.dumps(item_svg, ensure_ascii=False).encode('utf-8'))
#


# with open('./item_comments.json', 'rb') as f:
#     a = f.read()
# print(a.decode('utf-8'))
# a = json.loads(a.decode('utf-8'))
# print(len(a))
import requests
from lxml import etree
import json
import re
import time

#
# data = "<dd class=\"comment-post\" id=\"comment_3299053\"><div class=\"post-self\"><div class=\"jm-avatar\"><a href=\"javascript:\/\/;\"><img src=\"http:\/\/res.jiemian.com\/static\/dev\/img\/avatar\/369.jpg\" alt=\"\"><\/a><\/div><div class=\"comment-body\"><a href=\"javascript:\/\/;\" class=\"author-name\">\u6613\u8c61\u4e2d\u6b63<\/a><span><\/span><div class=\"comment-main\"><p>\u9020\u8f66\u65e0\u8def\u53ef\u8d70\uff0c\u62e5\u5835\u9020\u5c31\u52a8\u8f66\uff0c\u52a8\u8f66\u884c\u5728\u94c1\u8f68\u4e0a\uff0c\u54b1\u4eec\u52a8\u8f66\u505c\u8def\u4e0a\u3002\u51e0\u8fd1\u9971\u548c\uff0c\u591a\u8c22\u5173\u7167\uff01<\/p><\/div><div class=\"comment-footer\"><span class=\"date\">\u6628\u592913:31<\/span><span class=\"show-arrow\" style=\"width:13px;\"><\/span><span class=\"comment\" onclick=\"showCommentReply(3299053,0)\" id=\"showtype_3299053\" cid=\"3299053\" showtype='1'><a href=\"javascript:void(0)\">\u56de\u590d<\/a><em id=\"reply_count3299053\" >(0)<\/em><input type=\"hidden\" id=\"reply_count_hidden3299053\" value=\"\"\/><\/span><span class=\"like\" onclick=\"addPraise(3299053);\"><a href=\"javascript:void(0)\" class=\"heart jia-1\" title=\"\u8d5e\"   id='jia-3299053'>\u8d5e<\/a><em id=\"praise3299053\">(1)<\/em><\/span><span class=\"report\"><a href='javascript:void(0)' cid='3299053' id='show_ju_bao_div3299053'  class='show_ju-bao-btn'>\u4e3e\u62a5<\/a><\/span><span class=\"report\" style=\"display: block;position: relative\"><div class=\"ju-bao-box\" id=\"ju-bao-box3299053\"><div class=\"input-group\"><div class=\"pull-left\">\u4e3e\u62a5\u539f\u56e0<\/div><div class=\"radio\"><label><input type=\"radio\" name=\"industry3299053\" value=\"1\" checked=\"checked\">\u5783\u573e\u5e7f\u544a<\/label><\/div><div class=\"radio\"><label><input type=\"radio\" name=\"industry3299053\" value=\"2\">\u653f\u6cbb\u654f\u611f<\/label><\/div><div class=\"radio\"><label><input type=\"radio\" name=\"industry3299053\" value=\"3\">\u8272\u60c5\u66b4\u529b<\/label><\/div><div class=\"radio\"><label><input type=\"radio\" name=\"industry3299053\" value=\"4\">\u5176\u4ed6<\/label><\/div><br><div class=\"text-center\" style=\"margin-top: 10px;\"><button type=\"button\" class=\"addindustry\" id=\"addindustry\" cid=\"3299053\">\u63d0\u4ea4<\/button><\/div><\/div><\/div><\/span><span class=\"delete\"><\/span><\/div><\/div><\/div><div class=\"report-view\" id=\"report-view-3299053\" ><div class=\"report-box\" id=\"showReply_3299053\"  style=\"display:none;\"><div class=\"textarea-box\"><textarea class=\"textarea\" placeholder=\"\" id=\"reply_comment3299053\"><\/textarea><\/div><div class=\"textarea-btn-box\" id=\"addCommentButton3299053\"><button type=\"button\" class=\"btn\" onclick=\"addCommentReply(3299053,2598846,3299053);\">\u56de\u590d<\/button><\/div><\/div><!-- \u663e\u793a\u56de\u590d\u5185\u5bb9 --><ul class=\"reply-view\" id=\"reply-view3299053\"><span id=\"after\"><\/span><!--\u7528\u4e8e\u8ffd\u52a0\u5168\u90e8\u8bc4\u8bba\u7684\u6807\u793a--><\/ul><\/div><\/dd><dd class=\"comment-post\" id=\"comment_3299052\"><div class=\"post-self\"><div class=\"jm-avatar\"><a href=\"javascript:\/\/;\"><img src=\"http:\/\/res.jiemian.com\/static\/dev\/img\/avatar\/671.jpg\" alt=\"\"><\/a><\/div><div class=\"comment-body\"><a href=\"javascript:\/\/;\" class=\"author-name\">\u8d85\u8d8a\u81ea\u6211<\/a><span><\/span><div class=\"comment-main\"><p>\u94b1\u88ab\u623f\u5b50\u6dd8\u7a7a\u4e86<\/p><\/div><div class=\"comment-footer\"><span class=\"date\">\u6628\u592913:31<\/span><span class=\"show-arrow\" style=\"width:13px;\"><\/span><span class=\"comment\" onclick=\"showCommentReply(3299052,0)\" id=\"showtype_3299052\" cid=\"3299052\" showtype='1'><a href=\"javascript:void(0)\">\u56de\u590d<\/a><em id=\"reply_count3299052\" >(0)<\/em><input type=\"hidden\" id=\"reply_count_hidden3299052\" value=\"\"\/><\/span><span class=\"like\" onclick=\"addPraise(3299052);\"><a href=\"javascript:void(0)\" class=\"heart jia-1\" title=\"\u8d5e\"   id='jia-3299052'>\u8d5e<\/a><em id=\"praise3299052\">(0)<\/em><\/span><span class=\"report\"><a href='javascript:void(0)' cid='3299052' id='show_ju_bao_div3299052'  class='show_ju-bao-btn'>\u4e3e\u62a5<\/a><\/span><span class=\"report\" style=\"display: block;position: relative\"><div class=\"ju-bao-box\" id=\"ju-bao-box3299052\"><div class=\"input-group\"><div class=\"pull-left\">\u4e3e\u62a5\u539f\u56e0<\/div><div class=\"radio\"><label><input type=\"radio\" name=\"industry3299052\" value=\"1\" checked=\"checked\">\u5783\u573e\u5e7f\u544a<\/label><\/div><div class=\"radio\"><label><input type=\"radio\" name=\"industry3299052\" value=\"2\">\u653f\u6cbb\u654f\u611f<\/label><\/div><div class=\"radio\"><label><input type=\"radio\" name=\"industry3299052\" value=\"3\">\u8272\u60c5\u66b4\u529b<\/label><\/div><div class=\"radio\"><label><input type=\"radio\" name=\"industry3299052\" value=\"4\">\u5176\u4ed6<\/label><\/div><br><div class=\"text-center\" style=\"margin-top: 10px;\"><button type=\"button\" class=\"addindustry\" id=\"addindustry\" cid=\"3299052\">\u63d0\u4ea4<\/button><\/div><\/div><\/div><\/span><span class=\"delete\"><\/span><\/div><\/div><\/div><div class=\"report-view\" id=\"report-view-3299052\" ><div class=\"report-box\" id=\"showReply_3299052\"  style=\"display:none;\"><div class=\"textarea-box\"><textarea class=\"textarea\" placeholder=\"\" id=\"reply_comment3299052\"><\/textarea><\/div><div class=\"textarea-btn-box\" id=\"addCommentButton3299052\"><button type=\"button\" class=\"btn\" onclick=\"addCommentReply(3299052,2598846,3299052);\">\u56de\u590d<\/button><\/div><\/div><!-- \u663e\u793a\u56de\u590d\u5185\u5bb9 --><ul class=\"reply-view\" id=\"reply-view3299052\"><span id=\"after\"><\/span><!--\u7528\u4e8e\u8ffd\u52a0\u5168\u90e8\u8bc4\u8bba\u7684\u6807\u793a--><\/ul><\/div><\/dd><dd class=\"comment-post\" id=\"comment_3299051\"><div class=\"post-self\"><div class=\"jm-avatar\"><a href=\"javascript:\/\/;\"><img src=\"http:\/\/res.jiemian.com\/static\/dev\/img\/avatar\/515.jpg\" alt=\"\"><\/a><\/div><div class=\"comment-body\"><a href=\"javascript:\/\/;\" class=\"author-name\">ice kiss<\/a><span><\/span><div class=\"comment-main\"><p>\u5546\u5bb6\u8be5\u60f3\u7684\u8fd8\u662f\u5982\u4f55\u8f6c\u578b\u3002\u3002\u4e0d\u8981\u53ea\u662f\u5356\u8f66\u3002\u3002\u5360\u9886\u5e02\u573a\u8fbe\u5230\u9884\u671f\u4fdd\u6709\u91cf\uff0c\u8fd8\u662f\u5f97\u670d\u52a1\u4e3a\u4e3b\uff0c\u8fd9\u624d\u662f\u6e90\u6e90\u4e0d\u65ad\u7684\u8d22\u6e90\u3002<\/p><\/div><div class=\"comment-footer\"><span class=\"date\">\u6628\u592913:31<\/span><span class=\"show-arrow\" style=\"width:13px;\"><\/span><span class=\"comment\" onclick=\"showCommentReply(3299051,0)\" id=\"showtype_3299051\" cid=\"3299051\" showtype='1'><a href=\"javascript:void(0)\">\u56de\u590d<\/a><em id=\"reply_count3299051\" >(0)<\/em><input type=\"hidden\" id=\"reply_count_hidden3299051\" value=\"\"\/><\/span><span class=\"like\" onclick=\"addPraise(3299051);\"><a href=\"javascript:void(0)\" class=\"heart jia-1\" title=\"\u8d5e\"   id='jia-3299051'>\u8d5e<\/a><em id=\"praise3299051\">(0)<\/em><\/span><span class=\"report\"><a href='javascript:void(0)' cid='3299051' id='show_ju_bao_div3299051'  class='show_ju-bao-btn'>\u4e3e\u62a5<\/a><\/span><span class=\"report\" style=\"display: block;position: relative\"><div class=\"ju-bao-box\" id=\"ju-bao-box3299051\"><div class=\"input-group\"><div class=\"pull-left\">\u4e3e\u62a5\u539f\u56e0<\/div><div class=\"radio\"><label><input type=\"radio\" name=\"industry3299051\" value=\"1\" checked=\"checked\">\u5783\u573e\u5e7f\u544a<\/label><\/div><div class=\"radio\"><label><input type=\"radio\" name=\"industry3299051\" value=\"2\">\u653f\u6cbb\u654f\u611f<\/label><\/div><div class=\"radio\"><label><input type=\"radio\" name=\"industry3299051\" value=\"3\">\u8272\u60c5\u66b4\u529b<\/label><\/div><div class=\"radio\"><label><input type=\"radio\" name=\"industry3299051\" value=\"4\">\u5176\u4ed6<\/label><\/div><br><div class=\"text-center\" style=\"margin-top: 10px;\"><button type=\"button\" class=\"addindustry\" id=\"addindustry\" cid=\"3299051\">\u63d0\u4ea4<\/button><\/div><\/div><\/div><\/span><span class=\"delete\"><\/span><\/div><\/div><\/div><div class=\"report-view\" id=\"report-view-3299051\" ><div class=\"report-box\" id=\"showReply_3299051\"  style=\"display:none;\"><div class=\"textarea-box\"><textarea class=\"textarea\" placeholder=\"\" id=\"reply_comment3299051\"><\/textarea><\/div><div class=\"textarea-btn-box\" id=\"addCommentButton3299051\"><button type=\"button\" class=\"btn\" onclick=\"addCommentReply(3299051,2598846,3299051);\">\u56de\u590d<\/button><\/div><\/div><!-- \u663e\u793a\u56de\u590d\u5185\u5bb9 --><ul class=\"reply-view\" id=\"reply-view3299051\"><span id=\"after\"><\/span><!--\u7528\u4e8e\u8ffd\u52a0\u5168\u90e8\u8bc4\u8bba\u7684\u6807\u793a--><\/ul><\/div><\/dd><dd class=\"comment-post\" id=\"comment_3298535\"><div class=\"post-self\"><div class=\"jm-avatar\"><a href=\"javascript:\/\/;\"><img src=\"http:\/\/res.jiemian.com\/static\/dev\/img\/avatar\/147.jpg\" alt=\"\"><\/a><\/div><div class=\"comment-body\"><a href=\"javascript:\/\/;\" class=\"author-name\">\ud83c\udf42<\/a><span><\/span><div class=\"comment-main\"><p>\u6211\u611f\u89c9\u6469\u6258\u8f66\u8981\u6da8\u4ef7<\/p><\/div><div class=\"comment-footer\"><span class=\"date\">\u6628\u592913:01<\/span><span class=\"show-arrow\" style=\"width:13px;\"><\/span><span class=\"comment\" onclick=\"showCommentReply(3298535,0)\" id=\"showtype_3298535\" cid=\"3298535\" showtype='1'><a href=\"javascript:void(0)\">\u56de\u590d<\/a><em id=\"reply_count3298535\" >(0)<\/em><input type=\"hidden\" id=\"reply_count_hidden3298535\" value=\"\"\/><\/span><span class=\"like\" onclick=\"addPraise(3298535);\"><a href=\"javascript:void(0)\" class=\"heart jia-1\" title=\"\u8d5e\"   id='jia-3298535'>\u8d5e<\/a><em id=\"praise3298535\">(0)<\/em><\/span><span class=\"report\"><a href='javascript:void(0)' cid='3298535' id='show_ju_bao_div3298535'  class='show_ju-bao-btn'>\u4e3e\u62a5<\/a><\/span><span class=\"report\" style=\"display: block;position: relative\"><div class=\"ju-bao-box\" id=\"ju-bao-box3298535\"><div class=\"input-group\"><div class=\"pull-left\">\u4e3e\u62a5\u539f\u56e0<\/div><div class=\"radio\"><label><input type=\"radio\" name=\"industry3298535\" value=\"1\" checked=\"checked\">\u5783\u573e\u5e7f\u544a<\/label><\/div><div class=\"radio\"><label><input type=\"radio\" name=\"industry3298535\" value=\"2\">\u653f\u6cbb\u654f\u611f<\/label><\/div><div class=\"radio\"><label><input type=\"radio\" name=\"industry3298535\" value=\"3\">\u8272\u60c5\u66b4\u529b<\/label><\/div><div class=\"radio\"><label><input type=\"radio\" name=\"industry3298535\" value=\"4\">\u5176\u4ed6<\/label><\/div><br><div class=\"text-center\" style=\"margin-top: 10px;\"><button type=\"button\" class=\"addindustry\" id=\"addindustry\" cid=\"3298535\">\u63d0\u4ea4<\/button><\/div><\/div><\/div><\/span><span class=\"delete\"><\/span><\/div><\/div><\/div><div class=\"report-view\" id=\"report-view-3298535\" ><div class=\"report-box\" id=\"showReply_3298535\"  style=\"display:none;\"><div class=\"textarea-box\"><textarea class=\"textarea\" placeholder=\"\" id=\"reply_comment3298535\"><\/textarea><\/div><div class=\"textarea-btn-box\" id=\"addCommentButton3298535\"><button type=\"button\" class=\"btn\" onclick=\"addCommentReply(3298535,2598846,3298535);\">\u56de\u590d<\/button><\/div><\/div><!-- \u663e\u793a\u56de\u590d\u5185\u5bb9 --><ul class=\"reply-view\" id=\"reply-view3298535\"><span id=\"after\"><\/span><!--\u7528\u4e8e\u8ffd\u52a0\u5168\u90e8\u8bc4\u8bba\u7684\u6807\u793a--><\/ul><\/div><\/dd><dd class=\"comment-post\" id=\"comment_3298534\"><div class=\"post-self\"><div class=\"jm-avatar\"><a href=\"javascript:\/\/;\"><img src=\"http:\/\/res.jiemian.com\/static\/dev\/img\/avatar\/248.jpg\" alt=\"\"><\/a><\/div><div class=\"comment-body\"><a href=\"javascript:\/\/;\" class=\"author-name\">\u6a59\u5149<\/a><span><\/span><div class=\"comment-main\"><p>\u8f66\u771f\u662f\u6d88\u8017\u54c1\uff01\u6211\u5e73\u65f6\u4e0d\u600e\u4e48\u5f00 \u8981\u5f00\u57fa\u672c\u53bb\u8d2d\u7269\u7684 \u4e00\u4e2a\u6708\u4e09\u767e\u7684\u6cb9 \u90a3\u4e9b\u5929\u5929\u5f00\u53bb\u4e0a\u73ed\u7684\u4f30\u8ba1\u4e00\u4e2a\u793c\u62dc\u5c31\u4e94\u767e\u5757\u6cb9\u4e86 \u8fd8\u6709\u5916\u9762\u4e00\u767e\u4e0d\u5230\u7684\u505c\u8f66\u8d39 \u5c0f\u533a\u91cc\u7684\u4e00\u767e\u591a\u4e00\u4e2a\u6708\u7684\u505c\u8f66\u8d39 \u5dee\u4e0d\u591a\u4e00\u4e2a\u6708\u4e00\u5343\u5757 \u672c\u6765\u6253\u7b97\u4e0d\u60f3\u4e70\u8f66\u7684 \u540e\u6765\u5bb6\u91cc\u7236\u6bcd\u8981\u770b\u75c5\u817f\u811a\u4e0d\u65b9\u4fbf \u8001\u662f\u53eb\u4eb2\u621a\u5e2e\u5fd9\u5e26\u8fc7\u53bb\u4e5f\u96be\u4e3a\u60c5\u5c31\u5e72\u8106\u4e70\u4e86\u4e00\u8f86 \u4e0d\u8981\u542c\u7f51\u4e0a\u7684\u8bf4\u8f66\u4e0d\u597d\u4e0d\u8981\u4e70\u4ec0\u4e48\u4ec0\u4e48\u7684 \u4e00\u4e2a\u5bb6\u5ead\u5fc5\u987b\u8981\u6709\u4e00\u8f86\u8f66 \u5229\u5927\u4e8e\u5f0a\uff01\u6709\u8f66\u7edd\u5bf9\u662f\u597d\u4e8b\uff01<\/p><\/div><div class=\"comment-footer\"><span class=\"date\">\u6628\u592913:01<\/span><span class=\"show-arrow\" style=\"width:13px;\"><\/span><span class=\"comment\" onclick=\"showCommentReply(3298534,0)\" id=\"showtype_3298534\" cid=\"3298534\" showtype='1'><a href=\"javascript:void(0)\">\u56de\u590d<\/a><em id=\"reply_count3298534\" >(0)<\/em><input type=\"hidden\" id=\"reply_count_hidden3298534\" value=\"\"\/><\/span><span class=\"like\" onclick=\"addPraise(3298534);\"><a href=\"javascript:void(0)\" class=\"heart jia-1\" title=\"\u8d5e\"   id='jia-3298534'>\u8d5e<\/a><em id=\"praise3298534\">(0)<\/em><\/span><span class=\"report\"><a href='javascript:void(0)' cid='3298534' id='show_ju_bao_div3298534'  class='show_ju-bao-btn'>\u4e3e\u62a5<\/a><\/span><span class=\"report\" style=\"display: block;position: relative\"><div class=\"ju-bao-box\" id=\"ju-bao-box3298534\"><div class=\"input-group\"><div class=\"pull-left\">\u4e3e\u62a5\u539f\u56e0<\/div><div class=\"radio\"><label><input type=\"radio\" name=\"industry3298534\" value=\"1\" checked=\"checked\">\u5783\u573e\u5e7f\u544a<\/label><\/div><div class=\"radio\"><label><input type=\"radio\" name=\"industry3298534\" value=\"2\">\u653f\u6cbb\u654f\u611f<\/label><\/div><div class=\"radio\"><label><input type=\"radio\" name=\"industry3298534\" value=\"3\">\u8272\u60c5\u66b4\u529b<\/label><\/div><div class=\"radio\"><label><input type=\"radio\" name=\"industry3298534\" value=\"4\">\u5176\u4ed6<\/label><\/div><br><div class=\"text-center\" style=\"margin-top: 10px;\"><button type=\"button\" class=\"addindustry\" id=\"addindustry\" cid=\"3298534\">\u63d0\u4ea4<\/button><\/div><\/div><\/div><\/span><span class=\"delete\"><\/span><\/div><\/div><\/div><div class=\"report-view\" id=\"report-view-3298534\" ><div class=\"report-box\" id=\"showReply_3298534\"  style=\"display:none;\"><div class=\"textarea-box\"><textarea class=\"textarea\" placeholder=\"\" id=\"reply_comment3298534\"><\/textarea><\/div><div class=\"textarea-btn-box\" id=\"addCommentButton3298534\"><button type=\"button\" class=\"btn\" onclick=\"addCommentReply(3298534,2598846,3298534);\">\u56de\u590d<\/button><\/div><\/div><!-- \u663e\u793a\u56de\u590d\u5185\u5bb9 --><ul class=\"reply-view\" id=\"reply-view3298534\"><span id=\"after\"><\/span><!--\u7528\u4e8e\u8ffd\u52a0\u5168\u90e8\u8bc4\u8bba\u7684\u6807\u793a--><\/ul><\/div><\/dd><div class=\"pagination\"><ul><li><a  href=\"javascript:getListComment(1);\"><i>\u25c4<\/i><\/a><\/li><li><a  href=\"javascript:getListComment(1);\">1<\/a><\/li><li class=\"active\"><a>2<\/a><\/li><li><a  href=\"javascript:getListComment(3);\">3<\/a><\/li><li><a  href=\"javascript:getListComment(4);\">4<\/a><\/li><li><a  href=\"javascript:getListComment(5);\">5<\/a><\/li><li><a  href=\"javascript:getListComment(6);\">6<\/a><\/li><li><a  href=\"javascript:getListComment(7);\">7<\/a><\/li><li><a  href=\"javascript:getListComment(8);\">8<\/a><\/li><li><a  href=\"javascript:getListComment(3);\"><i>\u25ba<\/i><\/a><\/li><\/ul><\/div>"
# data = etree.HTML(data)
# print(data)
# data_list = data.xpath('.//dd[@class="comment-post"]')
# for data in data_list:
#     name = data.xpath('.//div[@class="comment-body"]/a/text()')
#     text = data.xpath('.//div[1]/p/text()')
#     print(name[0])
#     print(text[0])
# for i in range(1,5):
#     print(i)

# data_one = """jQuery1102019542031657240555_1541668100100({"message":"\u6210\u529f\uff01","code":0,"rs":"<dd class=\"comment-post\" id=\"comment_3298533\"><div class=\"post-self\"><div class=\"jm-avatar\"><a href=\"javascript:\/\/;\"><img src=\"http:\/\/res.jiemian.com\/static\/dev\/img\/avatar\/307.jpg\" alt=\"\"><\/a><\/div><div class=\"comment-body\"><a href=\"javascript:\/\/;\" class=\"author-name\">akuka lee<\/a><span><\/span><div class=\"comment-main\"><p>\u5343\u4e07\u522b\u4e70\uff0c\u6ca1\u5730\u65b9\u505c\uff0c\u80fd\u627e\u5230\u4e00\u5904\u5730\uff0c\u6536\u8d39\u8d35\u800c\u4e14\u8fdc\uff0c\u5e72\u8106\u81ea\u884c\u8f66\uff0c\u5730\u94c1\uff0c\u6253\u8f66\uff0c<\/p><\/div><div class=\"comment-footer\"><span class=\"date\">\u6628\u592913:01<\/span><span class=\"show-arrow\" style=\"width:13px;\"><\/span><span class=\"comment\" onclick=\"showCommentReply(3298533,0)\" id=\"showtype_3298533\" cid=\"3298533\" showtype='1'><a href=\"javascript:void(0)\">\u56de\u590d<\/a><em id=\"reply_count3298533\" >(0)<\/em><input type=\"hidden\" id=\"reply_count_hidden3298533\" value=\"\"\/><\/span><span class=\"like\" onclick=\"addPraise(3298533);\"><a href=\"javascript:void(0)\" class=\"heart jia-1\" title=\"\u8d5e\"   id='jia-3298533'>\u8d5e<\/a><em id=\"praise3298533\">(0)<\/em><\/span><span class=\"report\"><a href='javascript:void(0)' cid='3298533' id='show_ju_bao_div3298533'  class='show_ju-bao-btn'>\u4e3e\u62a5<\/a><\/span><span class=\"report\" style=\"display: block;position: relative\"><div class=\"ju-bao-box\" id=\"ju-bao-box3298533\"><div class=\"input-group\"><div class=\"pull-left\">\u4e3e\u62a5\u539f\u56e0<\/div><div class=\"radio\"><label><input type=\"radio\" name=\"industry3298533\" value=\"1\" checked=\"checked\">\u5783\u573e\u5e7f\u544a<\/label><\/div><div class=\"radio\"><label><input type=\"radio\" name=\"industry3298533\" value=\"2\">\u653f\u6cbb\u654f\u611f<\/label><\/div><div class=\"radio\"><label><input type=\"radio\" name=\"industry3298533\" value=\"3\">\u8272\u60c5\u66b4\u529b<\/label><\/div><div class=\"radio\"><label><input type=\"radio\" name=\"industry3298533\" value=\"4\">\u5176\u4ed6<\/label><\/div><br><div class=\"text-center\" style=\"margin-top: 10px;\"><button type=\"button\" class=\"addindustry\" id=\"addindustry\" cid=\"3298533\">\u63d0\u4ea4<\/button><\/div><\/div><\/div><\/span><span class=\"delete\"><\/span><\/div><\/div><\/div><div class=\"report-view\" id=\"report-view-3298533\" ><div class=\"report-box\" id=\"showReply_3298533\"  style=\"display:none;\"><div class=\"textarea-box\"><textarea class=\"textarea\" placeholder=\"\" id=\"reply_comment3298533\"><\/textarea><\/div><div class=\"textarea-btn-box\" id=\"addCommentButton3298533\"><button type=\"button\" class=\"btn\" onclick=\"addCommentReply(3298533,2598846,3298533);\">\u56de\u590d<\/button><\/div><\/div><!-- \u663e\u793a\u56de\u590d\u5185\u5bb9 --><ul class=\"reply-view\" id=\"reply-view3298533\"><span id=\"after\"><\/span><!--\u7528\u4e8e\u8ffd\u52a0\u5168\u90e8\u8bc4\u8bba\u7684\u6807\u793a--><\/ul><\/div><\/dd><dd class=\"comment-post\" id=\"comment_3298532\"><div class=\"post-self\"><div class=\"jm-avatar\"><a href=\"javascript:\/\/;\"><img src=\"http:\/\/res.jiemian.com\/static\/dev\/img\/avatar\/497.jpg\" alt=\"\"><\/a><\/div><div class=\"comment-body\"><a href=\"javascript:\/\/;\" class=\"author-name\">\ud83c\udf42<\/a><span><\/span><div class=\"comment-main\"><p>\u672a\u6765\u6469\u6258\u8f66\u7684\u5e02\u573a\u7279\u522b\u597d\uff01<\/p><\/div><div class=\"comment-footer\"><span class=\"date\">\u6628\u592913:01<\/span><span class=\"show-arrow\" style=\"width:13px;\"><\/span><span class=\"comment\" onclick=\"showCommentReply(3298532,0)\" id=\"showtype_3298532\" cid=\"3298532\" showtype='1'><a href=\"javascript:void(0)\">\u56de\u590d<\/a><em id=\"reply_count3298532\" >(0)<\/em><input type=\"hidden\" id=\"reply_count_hidden3298532\" value=\"\"\/><\/span><span class=\"like\" onclick=\"addPraise(3298532);\"><a href=\"javascript:void(0)\" class=\"heart jia-1\" title=\"\u8d5e\"   id='jia-3298532'>\u8d5e<\/a><em id=\"praise3298532\">(0)<\/em><\/span><span class=\"report\"><a href='javascript:void(0)' cid='3298532' id='show_ju_bao_div3298532'  class='show_ju-bao-btn'>\u4e3e\u62a5<\/a><\/span><span class=\"report\" style=\"display: block;position: relative\"><div class=\"ju-bao-box\" id=\"ju-bao-box3298532\"><div class=\"input-group\"><div class=\"pull-left\">\u4e3e\u62a5\u539f\u56e0<\/div><div class=\"radio\"><label><input type=\"radio\" name=\"industry3298532\" value=\"1\" checked=\"checked\">\u5783\u573e\u5e7f\u544a<\/label><\/div><div class=\"radio\"><label><input type=\"radio\" name=\"industry3298532\" value=\"2\">\u653f\u6cbb\u654f\u611f<\/label><\/div><div class=\"radio\"><label><input type=\"radio\" name=\"industry3298532\" value=\"3\">\u8272\u60c5\u66b4\u529b<\/label><\/div><div class=\"radio\"><label><input type=\"radio\" name=\"industry3298532\" value=\"4\">\u5176\u4ed6<\/label><\/div><br><div class=\"text-center\" style=\"margin-top: 10px;\"><button type=\"button\" class=\"addindustry\" id=\"addindustry\" cid=\"3298532\">\u63d0\u4ea4<\/button><\/div><\/div><\/div><\/span><span class=\"delete\"><\/span><\/div><\/div><\/div><div class=\"report-view\" id=\"report-view-3298532\" ><div class=\"report-box\" id=\"showReply_3298532\"  style=\"display:none;\"><div class=\"textarea-box\"><textarea class=\"textarea\" placeholder=\"\" id=\"reply_comment3298532\"><\/textarea><\/div><div class=\"textarea-btn-box\" id=\"addCommentButton3298532\"><button type=\"button\" class=\"btn\" onclick=\"addCommentReply(3298532,2598846,3298532);\">\u56de\u590d<\/button><\/div><\/div><!-- \u663e\u793a\u56de\u590d\u5185\u5bb9 --><ul class=\"reply-view\" id=\"reply-view3298532\"><span id=\"after\"><\/span><!--\u7528\u4e8e\u8ffd\u52a0\u5168\u90e8\u8bc4\u8bba\u7684\u6807\u793a--><\/ul><\/div><\/dd><dd class=\"comment-post\" id=\"comment_3298530\"><div class=\"post-self\"><div class=\"jm-avatar\"><a href=\"javascript:\/\/;\"><img src=\"http:\/\/res.jiemian.com\/static\/dev\/img\/avatar\/249.jpg\" alt=\"\"><\/a><\/div><div class=\"comment-body\"><a href=\"javascript:\/\/;\" class=\"author-name\">\u6885\u603b\u3002<\/a><span><\/span><div class=\"comment-main\"><p>\u6211\u8eab\u8fb9\u7684\u670b\u53cb\u4eb2\u621a\u90fd\u6709\u8f66\u4f60\u53eb\u6211\u600e\u4e48\u4e0d\u60f3\u8981\u8f66\uff0c\u8fc7\u5e74\u5929\u6c14\u53c8\u51b7\u6ca1\u6709\u8f66\u6211\u90fd\u4e0d\u60f3\u53bb\u4eb2\u621a\u5bb6\u62dc\u5e74\u4e86\uff0c\u4eb2\u621a\u5bb6\u6709\u559c\u4e8b\u90fd\u662f\u5168\u5bb6\u51fa\u52a8\uff0c\u6ca1\u8f66\u600e\u4e48\u53bb\u3002<\/p><\/div><div class=\"comment-footer\"><span class=\"date\">\u6628\u592913:01<\/span><span class=\"show-arrow\" style=\"width:13px;\"><\/span><span class=\"comment\" onclick=\"showCommentReply(3298530,0)\" id=\"showtype_3298530\" cid=\"3298530\" showtype='1'><a href=\"javascript:void(0)\">\u56de\u590d<\/a><em id=\"reply_count3298530\" >(0)<\/em><input type=\"hidden\" id=\"reply_count_hidden3298530\" value=\"\"\/><\/span><span class=\"like\" onclick=\"addPraise(3298530);\"><a href=\"javascript:void(0)\" class=\"heart jia-1\" title=\"\u8d5e\"   id='jia-3298530'>\u8d5e<\/a><em id=\"praise3298530\">(0)<\/em><\/span><span class=\"report\"><a href='javascript:void(0)' cid='3298530' id='show_ju_bao_div3298530'  class='show_ju-bao-btn'>\u4e3e\u62a5<\/a><\/span><span class=\"report\" style=\"display: block;position: relative\"><div class=\"ju-bao-box\" id=\"ju-bao-box3298530\"><div class=\"input-group\"><div class=\"pull-left\">\u4e3e\u62a5\u539f\u56e0<\/div><div class=\"radio\"><label><input type=\"radio\" name=\"industry3298530\" value=\"1\" checked=\"checked\">\u5783\u573e\u5e7f\u544a<\/label><\/div><div class=\"radio\"><label><input type=\"radio\" name=\"industry3298530\" value=\"2\">\u653f\u6cbb\u654f\u611f<\/label><\/div><div class=\"radio\"><label><input type=\"radio\" name=\"industry3298530\" value=\"3\">\u8272\u60c5\u66b4\u529b<\/label><\/div><div class=\"radio\"><label><input type=\"radio\" name=\"industry3298530\" value=\"4\">\u5176\u4ed6<\/label><\/div><br><div class=\"text-center\" style=\"margin-top: 10px;\"><button type=\"button\" class=\"addindustry\" id=\"addindustry\" cid=\"3298530\">\u63d0\u4ea4<\/button><\/div><\/div><\/div><\/span><span class=\"delete\"><\/span><\/div><\/div><\/div><div class=\"report-view\" id=\"report-view-3298530\" ><div class=\"report-box\" id=\"showReply_3298530\"  style=\"display:none;\"><div class=\"textarea-box\"><textarea class=\"textarea\" placeholder=\"\" id=\"reply_comment3298530\"><\/textarea><\/div><div class=\"textarea-btn-box\" id=\"addCommentButton3298530\"><button type=\"button\" class=\"btn\" onclick=\"addCommentReply(3298530,2598846,3298530);\">\u56de\u590d<\/button><\/div><\/div><!-- \u663e\u793a\u56de\u590d\u5185\u5bb9 --><ul class=\"reply-view\" id=\"reply-view3298530\"><span id=\"after\"><\/span><!--\u7528\u4e8e\u8ffd\u52a0\u5168\u90e8\u8bc4\u8bba\u7684\u6807\u793a--><\/ul><\/div><\/dd><dd class=\"comment-post\" id=\"comment_3298528\"><div class=\"post-self\"><div class=\"jm-avatar\"><a href=\"javascript:\/\/;\"><img src=\"http:\/\/res.jiemian.com\/static\/dev\/img\/avatar\/510.jpg\" alt=\"\"><\/a><\/div><div class=\"comment-body\"><a href=\"javascript:\/\/;\" class=\"author-name\">\u7b80\u7ea6<\/a><span><\/span><div class=\"comment-main\"><p>\u60f3\u4e70\u8f66\u7684\u6323\u4e0d\u5230\u94b1\u4e86\uff0c\u624d\u662f\u6700\u91cd\u8981\u7684\u5176\u6b21\u5c31\u662f\u6cb9\u4ef7\u3002<\/p><\/div><div class=\"comment-footer\"><span class=\"date\">\u6628\u592913:01<\/span><span class=\"show-arrow\" style=\"width:13px;\"><\/span><span class=\"comment\" onclick=\"showCommentReply(3298528,0)\" id=\"showtype_3298528\" cid=\"3298528\" showtype='1'><a href=\"javascript:void(0)\">\u56de\u590d<\/a><em id=\"reply_count3298528\" >(0)<\/em><input type=\"hidden\" id=\"reply_count_hidden3298528\" value=\"\"\/><\/span><span class=\"like\" onclick=\"addPraise(3298528);\"><a href=\"javascript:void(0)\" class=\"heart jia-1\" title=\"\u8d5e\"   id='jia-3298528'>\u8d5e<\/a><em id=\"praise3298528\">(0)<\/em><\/span><span class=\"report\"><a href='javascript:void(0)' cid='3298528' id='show_ju_bao_div3298528'  class='show_ju-bao-btn'>\u4e3e\u62a5<\/a><\/span><span class=\"report\" style=\"display: block;position: relative\"><div class=\"ju-bao-box\" id=\"ju-bao-box3298528\"><div class=\"input-group\"><div class=\"pull-left\">\u4e3e\u62a5\u539f\u56e0<\/div><div class=\"radio\"><label><input type=\"radio\" name=\"industry3298528\" value=\"1\" checked=\"checked\">\u5783\u573e\u5e7f\u544a<\/label><\/div><div class=\"radio\"><label><input type=\"radio\" name=\"industry3298528\" value=\"2\">\u653f\u6cbb\u654f\u611f<\/label><\/div><div class=\"radio\"><label><input type=\"radio\" name=\"industry3298528\" value=\"3\">\u8272\u60c5\u66b4\u529b<\/label><\/div><div class=\"radio\"><label><input type=\"radio\" name=\"industry3298528\" value=\"4\">\u5176\u4ed6<\/label><\/div><br><div class=\"text-center\" style=\"margin-top: 10px;\"><button type=\"button\" class=\"addindustry\" id=\"addindustry\" cid=\"3298528\">\u63d0\u4ea4<\/button><\/div><\/div><\/div><\/span><span class=\"delete\"><\/span><\/div><\/div><\/div><div class=\"report-view\" id=\"report-view-3298528\" ><div class=\"report-box\" id=\"showReply_3298528\"  style=\"display:none;\"><div class=\"textarea-box\"><textarea class=\"textarea\" placeholder=\"\" id=\"reply_comment3298528\"><\/textarea><\/div><div class=\"textarea-btn-box\" id=\"addCommentButton3298528\"><button type=\"button\" class=\"btn\" onclick=\"addCommentReply(3298528,2598846,3298528);\">\u56de\u590d<\/button><\/div><\/div><!-- \u663e\u793a\u56de\u590d\u5185\u5bb9 --><ul class=\"reply-view\" id=\"reply-view3298528\"><span id=\"after\"><\/span><!--\u7528\u4e8e\u8ffd\u52a0\u5168\u90e8\u8bc4\u8bba\u7684\u6807\u793a--><\/ul><\/div><\/dd><dd class=\"comment-post\" id=\"comment_3297787\"><div class=\"post-self\"><div class=\"jm-avatar\"><a href=\"javascript:\/\/;\"><img src=\"http:\/\/res.jiemian.com\/static\/dev\/img\/avatar\/213.jpg\" alt=\"\"><\/a><\/div><div class=\"comment-body\"><a href=\"javascript:\/\/;\" class=\"author-name\">\u4e91<\/a><span><\/span><div class=\"comment-main\"><p>\u6cb9\u6da8\u523015\u5143\u90a3\u5c31\u73af\u4fdd\u4e86\uff0c\u5168\u505c\u8f66<\/p><\/div><div class=\"comment-footer\"><span class=\"date\">\u6628\u592912:31<\/span><span class=\"show-arrow\" style=\"width:13px;\"><\/span><span class=\"comment\" onclick=\"showCommentReply(3297787,0)\" id=\"showtype_3297787\" cid=\"3297787\" showtype='1'><a href=\"javascript:void(0)\">\u56de\u590d<\/a><em id=\"reply_count3297787\" >(0)<\/em><input type=\"hidden\" id=\"reply_count_hidden3297787\" value=\"\"\/><\/span><span class=\"like\" onclick=\"addPraise(3297787);\"><a href=\"javascript:void(0)\" class=\"heart jia-1\" title=\"\u8d5e\"   id='jia-3297787'>\u8d5e<\/a><em id=\"praise3297787\">(0)<\/em><\/span><span class=\"report\"><a href='javascript:void(0)' cid='3297787' id='show_ju_bao_div3297787'  class='show_ju-bao-btn'>\u4e3e\u62a5<\/a><\/span><span class=\"report\" style=\"display: block;position: relative\"><div class=\"ju-bao-box\" id=\"ju-bao-box3297787\"><div class=\"input-group\"><div class=\"pull-left\">\u4e3e\u62a5\u539f\u56e0<\/div><div class=\"radio\"><label><input type=\"radio\" name=\"industry3297787\" value=\"1\" checked=\"checked\">\u5783\u573e\u5e7f\u544a<\/label><\/div><div class=\"radio\"><label><input type=\"radio\" name=\"industry3297787\" value=\"2\">\u653f\u6cbb\u654f\u611f<\/label><\/div><div class=\"radio\"><label><input type=\"radio\" name=\"industry3297787\" value=\"3\">\u8272\u60c5\u66b4\u529b<\/label><\/div><div class=\"radio\"><label><input type=\"radio\" name=\"industry3297787\" value=\"4\">\u5176\u4ed6<\/label><\/div><br><div class=\"text-center\" style=\"margin-top: 10px;\"><button type=\"button\" class=\"addindustry\" id=\"addindustry\" cid=\"3297787\">\u63d0\u4ea4<\/button><\/div><\/div><\/div><\/span><span class=\"delete\"><\/span><\/div><\/div><\/div><div class=\"report-view\" id=\"report-view-3297787\" ><div class=\"report-box\" id=\"showReply_3297787\"  style=\"display:none;\"><div class=\"textarea-box\"><textarea class=\"textarea\" placeholder=\"\" id=\"reply_comment3297787\"><\/textarea><\/div><div class=\"textarea-btn-box\" id=\"addCommentButton3297787\"><button type=\"button\" class=\"btn\" onclick=\"addCommentReply(3297787,2598846,3297787);\">\u56de\u590d<\/button><\/div><\/div><!-- \u663e\u793a\u56de\u590d\u5185\u5bb9 --><ul class=\"reply-view\" id=\"reply-view3297787\"><span id=\"after\"><\/span><!--\u7528\u4e8e\u8ffd\u52a0\u5168\u90e8\u8bc4\u8bba\u7684\u6807\u793a--><\/ul><\/div><\/dd><div class=\"pagination\"><ul><li><a  href=\"javascript:getListComment(2);\"><i>\u25c4<\/i><\/a><\/li><li><a  href=\"javascript:getListComment(1);\">1<\/a><\/li><li><a  href=\"javascript:getListComment(2);\">2<\/a><\/li><li class=\"active\"><a>3<\/a><\/li><li><a  href=\"javascript:getListComment(4);\">4<\/a><\/li><li><a  href=\"javascript:getListComment(5);\">5<\/a><\/li><li><a  href=\"javascript:getListComment(6);\">6<\/a><\/li><li><a  href=\"javascript:getListComment(7);\">7<\/a><\/li><li><a  href=\"javascript:getListComment(8);\">8<\/a><\/li><li><a  href=\"javascript:getListComment(4);\"><i>\u25ba<\/i><\/a><\/li><\/ul><\/div>","count":582,"ding":10,"collect":8,"user_status":null,"page_count":"92"})"""
# data_one = re.findall(r'<dd class=.*<\\/li><\\/ul><\\/div>', data_one)
# print(data_one)
# data_list = [i for i in data]
# print(data_list[2746],data_list[2747])
# data = data.split("(")[1:]
# data = ''.join(data)
# data = json.dumps(data)
# print(type(data))

comment_port_url = 'https://a.jiemian.com/index.php?m=comment&a=getlistCommentP&aid=2598846&page=1&comment_type=1&per_page=5&callback=jQuery110206352600736454153_1541740292475&_=1541740292483'
response = requests.get(comment_port_url)
data = response.content.decode()
data = re.sub(r'\\"', '\"', data)
print(data)
data = re.findall(r'<dd class=.*?/dd>', data)
for data in data:
    data = etree.HTML(data)
    data_list = data.xpath('.//dd[@class="comment-post"]')
    for data in data_list:
        name = data.xpath('.//div[@class="comment-body"]/a/text()')[0].encode('utf-8').decode('unicode_escape')
        text = data.xpath('.//div[1]/p/text()')[0].encode('utf-8').decode('unicode_escape')
        data_all = data.xpath('.//div[@class="comment-footer"]/span[1]/text()')[0]
        day_date = data_all.split(' ')[0]
        comment_time = data_all.split(' ')[1]
        day_date = re.sub(r'\\/', '-', day_date)
        # 点赞数
        likes = data.xpath('.//em/text()')[0]
        # 回复数
        comments_count = '0'
        print(name)
        print(text)
        print(day_date, comment_time, re.search('\d', likes).group(0))
# -*- coding: utf-8 -*-
import LineAlpha
from LineAlpha.lib.Gen.ttypes import Message
from datetime import datetime
from io import StringIO
import time,random,sys,json,codecs,threading,glob,sys
import re,string,datetime,os
import os.path,sys,urllib,shutil,subprocess

cl = LineAlpha.LINE()
cl.login(qr=True)
cl.loginResult()

ki = LineAlpha.LINE()
ki.login(qr=True)
ki.loginResult()

ki2 = LineAlpha.LINE()
ki2.login(qr=True)
ki2.loginResult()
print u"login success"
reload(sys)
sys.setdefaultencoding('utf-8')
helpMessage ="""
・[Id] : Menampilkan ID target.
・[Mid]: Menampilkan MID.
・[Me] : Saya akan mengirimkan informasi kontak saya.
・[TL:「Text」]: Poskan pada timeline.
・[Rename]： Ganti Nama anda.
・[Gift]: Saya akan mengirimkan hadiah kepada Anda.
・[Kontak:「mid」]: midMengkonversi kontak.
・[Group id]: Menampilkan id group.
・[Cancel]: Tolak undangan grup.
・[Kontak:on] : Kirim informasi setelah mengirim informasi kontak.
・[Kontak:off] : saya tidak akan mengirimkan informasinya.
・[Join:on] : Otomatis masuk Group.
・[Join:off] : Gak join group otomatis.
・[Cancel:「Jumlah orang」] : Undangan grup di bawah "jumlah orang" akan ditolak secara otomatis.
・[canjoin] : Izinkan semua undangan.
・[Paksa:on] : Keluar secara otomatis paksa.
・[Paksa:off] Jangan paksa putus secara paksa.
・[Add:on] : Tambah teman secara otomatis.
・[Add:off] : Matikan penambahan otomatis.
・[Pesan:「Text] : Ubah pesan untuk penambahan otomatis.
・[auto pesan] : Konfirmasikan pesan untuk penambahan otomatis.
・[b] : Blacklist.
・[bd] : Hapus dari blacklist.
・[bc] : Cek Blacklist user.
・[gbc] : Id blacklist.
・[bk] : Kill Blacklist.
・[Confirm]: Pastikan BOT setengah bergerak.


- Perintah berikut hanya bisa digunakan dalam Group -
・[urlon] : Buka QR.
・[urloff] :Tutup QR.
・[url] : lihat URL Group
・[url:「Group ID」] : Kami akan mengeluarkan URL undangan dari ID grup Anda.
・[Invite：「mid」] : Undang pengguna dengan mid yang ditentukan ke grup.
・[kick：「mid」] : Kick menggunakan mid yang ditentukan dari grup.
・[Ginfo] : Tampilan informasi grup.
・[Cancelall] :Batalkan semua pengguna yang diundang dalam grup.
・[Gn:「Text」] ： Mengubah nama grup.
・[NK:「Nama」] :Kick pengguna dengan nama yang ditentukan dari grup.
 """

mid = cl.getProfile().mid
kimid = ki.getProfile().mid
k2mid = ki2.getProfile().mid


wait = {
    'contact':True,
    'autoJoin':False,
    'autoCancel':{"on":True,"members":1},
    'leaveRoom':False,
    'timeline':True,
    'autoAdd':False,
    'message':"",
    "lang":"JP",
    "comment":"Pekok",
    "commentOn":True,
    "commentBlack":{},
    "wblack":False,
    "dblack":False,
    "clock":True,
    "cName":"тσ'ıʄ ",
    "blacklist":{},
    "wblacklist":False,
    "dblacklist":False
}

def bot(op):
    try:
        if op.type == 0:
            return
        if op.type == 5:
            if wait["autoAdd"] == True:
                cl.findAndAddContactsByMid(op.param1)
                if (wait["message"] in [""," ","\n",None]):
                    pass
                else:
                    cl.sendText(op.param1,str(wait["message"]))
        if op.type == 13:
            if mid in op.param3:
                G = cl.getGroup(op.param1)
                if wait["autoJoin"] == True:
                    if wait["autoCancel"]["on"] == True:
                        if len(G.members) <= wait["autoCancel"]["members"]:
                            cl.rejectGroupInvitation(op.param1)
                        else:
                            cl.acceptGroupInvitation(op.param1)
                    else:
                        cl.acceptGroupInvitation(op.param1)
                elif wait["autoCancel"]["on"] == True:
                    if len(G.members) <= wait["autoCancel"]["members"]:
                        cl.rejectGroupInvitation(op.param1)
            else:
                Inviter = op.param3.replace("",',')
                InviterX = Inviter.split(",")
                matched_list = []
                for tag in wait["blacklist"]:
                    matched_list+=filter(lambda str: str == tag, InviterX)
                if matched_list == []:
                    pass
                else:
                    cl.cancelGroupInvitation(op.param1, matched_list)
        if op.type == 19:
            if mid in op.param3:
                wait["blacklist"][op.param2] = True
        if op.type == 22:
            if wait["leaveRoom"] == True:
                cl.leaveRoom(op.param1)
        if op.type == 24:
            if wait["leaveRoom"] == True:
                cl.leaveRoom(op.param1)
        if op.type == 26:
            msg = op.message
            if msg.toType == 0:
                msg.to = msg.from_
                if msg.from_ == "u0c8779ca416157866099d62a8b583706":
                    if "join:" in msg.text:
                        list_ = msg.text.split(":")
                        try:
                            cl.acceptGroupInvitationByTicket(list_[1],list_[2])
                            G = cl.getGroup(list_[1])
                            G.preventJoinByTicket = True
                            cl.updateGroup(G)
                        except:
                            cl.sendText(msg.to,"error")
            if msg.toType == 1:
                if wait["leaveRoom"] == True:
                    cl.leaveRoom(msg.to)
            if msg.contentType == 16:
                url = msg.contentMetadata["postEndUrl"]
                cl.like(url[25:58], url[66:], likeType=1001)
        if op.type == 25:
            msg = op.message
            if msg.contentType == 13:
                if wait["wblack"] == True:
                    if msg.contentMetadata["mid"] in wait["commentBlack"]:
                        cl.sendText(msg.to,"すでにブラックリストに入っています。")
                        wait["wblack"] = False
                    else:
                        wait["commentBlack"][msg.contentMetadata["mid"]] = True
                        wait["wblack"] = False
                        cl.sendText(msg.to,"コメントしないようにしました。")
                        f=codecs.open('st2.json','w','utf-8')
                        json.dump(wait["commentBlack"], f, sort_keys=True, indent=4,ensure_ascii=False)
                elif wait["dblack"] == True:
                    if msg.contentMetadata["mid"] in wait["commentBlack"]:
                        del wait["commentBlack"][msg.contentMetadata["mid"]]
                        cl.sendText(msg.to,"ブラックリストから削除しました。")
                        wait["dblack"] = False
                        f=codecs.open('st2.json','w','utf-8')
                        json.dump(wait["commentBlack"], f, sort_keys=True, indent=4,ensure_ascii=False)
                    else:
                        wait["dblack"] = False
                        cl.sendText(msg.to,"ブラックリストに入っていません。")
                elif wait["wblacklist"] == True:
                    if msg.contentMetadata["mid"] in wait["blacklist"]:
                        cl.sendText(msg.to,"すでにブラックリストに入っています。")
                        wait["wblacklist"] = False
                    else:
                        wait["blacklist"][msg.contentMetadata["mid"]] = True
                        wait["wblacklist"] = False
                        cl.sendText(msg.to,"ブラックリストに追加しました。")
                        f=codecs.open('st2__b.json','w','utf-8')
                        json.dump(wait["blacklist"], f, sort_keys=True, indent=4,ensure_ascii=False)
                elif wait["dblacklist"] == True:
                    if msg.contentMetadata["mid"] in wait["blacklist"]:
                        del wait["blacklist"][msg.contentMetadata["mid"]]
                        cl.sendText(msg.to,"ブラックリストから削除しました。")
                        wait["dblacklist"] = False
                        f=codecs.open('st2__b.json','w','utf-8')
                        json.dump(wait["blacklist"], f, sort_keys=True, indent=4,ensure_ascii=False)
                    else:
                        wait["dblacklist"] = False
                        cl.sendText(msg.to,"ブラックリストに入っていません。")
                elif wait["contact"] == True:
                    msg.contentType = 0
                    cl.sendText(msg.to,msg.contentMetadata["mid"])
                    if 'displayName' in msg.contentMetadata:
                        contact = cl.getContact(msg.contentMetadata["mid"])
                        try:
                            cu = cl.channel.getCover(msg.contentMetadata["mid"])
                        except:
                            cu = ""
                        cl.sendText(msg.to,"[displayName]:\n" + msg.contentMetadata["displayName"] + "\n[mid]:\n" + msg.contentMetadata["mid"] + "\n[statusMessage]:\n" + contact.statusMessage + "\n[pictureStatus]:\nhttp://dl.profile.line-cdn.net/" + contact.pictureStatus + "\n[coverURL]:\n" + str(cu))
                    else:
                        contact = cl.getContact(msg.contentMetadata["mid"])
                        try:
                            cu = cl.channel.getCover(msg.contentMetadata["mid"])
                        except:
                            cu = ""
                        cl.sendText(msg.to,"[displayName]:\n" + contact.displayName + "\n[mid]:\n" + msg.contentMetadata["mid"] + "\n[statusMessage]:\n" + contact.statusMessage + "\n[pictureStatus]:\nhttp://dl.profile.line-cdn.net/" + contact.pictureStatus + "\n[coverURL]:\n" + str(cu))
            elif msg.contentType == 16:
                if wait["timeline"] == True:
                    msg.contentType = 0
                    if wait["lang"] == "JP":
                        msg.text = "URL\n" + msg.contentMetadata["postEndUrl"]
                    else:
                        msg.text = "URL→\n" + msg.contentMetadata["postEndUrl"]
                    cl.sendText(msg.to,msg.text)
            elif msg.text is None:
                return
            elif msg.text in ["help","ヘルプ","へるぷ"]:
                if wait["lang"] == "JP":
                    cl.sendText(msg.to,helpMessage)
                else:
                    cl.sendText(msg.to,helpt)
            elif ("Gn:" in msg.text):
                if msg.toType == 2:
                    group = cl.getGroup(msg.to)
                    group.name = msg.text.replace("Gn:","")
                    ki.updateGroup(group)
                else:
                    cl.sendText(msg.to,"グループ以外では使用できません。")
            elif ("群組名字變更→" in msg.text):
                if msg.toType == 2:
                    group = cl.getGroup(msg.to)
                    group.name = msg.text.replace("群組名字變更→","")
                    cl.updateGroup(group)
                else:
                    cl.sendText(msg.to,"以小组以外不能使用")
            elif "kick:" in msg.text:
                midd = msg.text.replace("kick:","")
                cl.kickoutFromGroup(msg.to,[midd])
            elif "招待:" in msg.text:
                midd = msg.text.replace("招待:","")
                cl.findAndAddContactsByMid(midd)
                cl.inviteIntoGroup(msg.to,[midd])
            elif "me" == msg.text:
                msg.contentType = 13
                msg.contentMetadata = {'mid': mid}
                cl.sendMessage(msg)
            elif msg.text in ["Gift","愛的禮物"]:
                msg.contentType = 9
                msg.contentMetadata={'PRDID': '3b92ccf5-54d3-4765-848f-c9ffdc1da020',
                                    'PRDTYPE': 'THEME',
                                    'MSGTPL': '5'}
                msg.text = None
                cl.sendMessage(msg)
            elif msg.text in ["キャンセル","cancel","取消邀請"]:
                if msg.toType == 2:
                    group = ki.getGroup(msg.to)
                    if group.invitee is not None:
                        gInviMids = [contact.mid for contact in group.invitee]
                        ki.cancelGroupInvitation(msg.to, gInviMids)
                    else:
                        if wait["lang"] == "JP":
                            cl.sendText(msg.to,"招待中の人はいません。")
                        else:
                            cl.sendText(msg.to,"邀请里面的人不在。")
                else:
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"グループ以外では使用できません。")
                    else:
                        cl.sendText(msg.to,"以小组以外不能使用")

            elif msg.text in ["#c-cancel"]:
                if msg.toType == 2:
                    group = cl.getGroup(msg.to)
                    if group.invitee is not None:
                        gInviMids = [contact.mid for contact in group.invitee]
                        cl.cancelGroupInvitation(msg.to, gInviMids)
                    else:
                        if wait["lang"] == "JP":
                            cl.sendText(msg.to,"招待中の人はいません。")
                        else:
                            cl.sendText(msg.to,"邀请里面的人不在。")
                else:
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"グループ以外では使用できません。")
                    else:
                        cl.sendText(msg.to,"以小组以外不能使用")
            #elif "gurl" == msg.text:
                #print cl.getGroup(msg.to)
                ##cl.sendMessage(msg)
            elif msg.text in ["urlon"]:
                if msg.toType == 2:
                    group = cl.getGroup(msg.to)
                    group.preventJoinByTicket = False
                    cl.updateGroup(group)
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"urlを許可しました。")
                    else:
                        cl.sendText(msg.to,"准许了URL。")
                else:
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"グループ以外では使用できません。")
                    else:
                        cl.sendText(msg.to,"以小组以外不能使用")
            elif msg.text in ["urloff"]:
                if msg.toType == 2:
                    group = cl.getGroup(msg.to)
                    group.preventJoinByTicket = True
                    cl.updateGroup(group)
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"urlを拒否しました。")
                    else:
                        cl.sendText(msg.to,"拒绝了URL。")
                else:
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"グループ以外では使用できません。")
                    else:
                        cl.sendText(msg.to,"以小组以外不能使用")
            elif msg.text == "グループ情報":
                if msg.toType == 2:
                    ginfo = cl.getGroup(msg.to)
                    try:
                        gCreator = ginfo.creator.displayName
                    except:
                        gCreator = "Error"
                    if wait["lang"] == "JP":
                        if ginfo.invitee is None:
                            sinvitee = "0"
                        else:
                            sinvitee = str(len(ginfo.invitee))
                        if ginfo.preventJoinByTicket == True:
                            u = "拒否"
                        else:
                            u = "許可"
                        cl.sendText(msg.to,"[名前]\n" + str(ginfo.name) + "\n[gid]\n" + msg.to + "\n[グループの作成者]\n" + gCreator + "\n[グループアイコン]\nhttp://dl.profile.line.naver.jp/" + ginfo.pictureStatus + "\nメンバー:" + str(len(ginfo.members)) + "人\n招待中:" + sinvitee + "人\n招待URL:" + u + "中です。")
                    else:
                        cl.sendText(msg.to,"[名字]\n" + str(ginfo.name) + "\n[gid]\n" + msg.to + "\n[小组的作成者]\n" + gCreator + "\n[小组图标]\nhttp://dl.profile.line.naver.jp/" + ginfo.pictureStatus)
                else:
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"グループ以外では使用できません。")
                    else:
                        cl.sendText(msg.to,"以小组以外不能使用")
            elif "id" == msg.text:
                cl.sendText(msg.to,msg.to)
            elif "mid" == msg.text:
                cl.sendText(msg.to,mid)
                ki.sendText(msg.to,kimid)
                ki2.sendText(msg.to,k2mid)

            elif "り" == msg.text:
                msg.contentType = 7
                msg.text = None
                msg.contentMetadata = {
                                     "STKID": "12623182_",
                                     "STKPKGID": "2",
                                      }
                cl.sendMessage(msg)
            elif "ダメ" == msg.text:
                msg.contentType = 7
                msg.text = None
                msg.contentMetadata = {
                                     "STKID": "12623183_",
                                     "STKPKGID": "2",
                                      }
                cl.sendMessage(msg)
            elif "少女祈祷中" == msg.text:
                msg.contentType = 7
                msg.text = None
                msg.contentMetadata = {
                                     "STKID": "12623191_",
                                     "STKPKGID": "2",
                                      }
                cl.sendMessage(msg)
            elif "TL→" in msg.text:
                tl_text = msg.text.replace("TL→","")
                cl.sendText(msg.to,"line://home/post?userMid="+mid+"&postId="+cl.new_post(tl_text)["result"]["post"]["postInfo"]["postId"])
            elif "cl名前変更:" in msg.text:
                string = msg.text.replace("cl名前変更:","")
                if len(string.decode('utf-8')) <= 20:
                    profile = cl.getProfile()
                    profile.displayName = string
                    cl.updateProfile(profile)
                    cl.sendText(msg.to,"名前を" + string + "に変更しました。")
            elif "我的名字" in msg.text:
                string = msg.text.replace("我的名字","")
                if len(string.decode('utf-8')) <= 20:
                    profile = cl.getProfile()
                    profile.displayName = string
                    cl.updateProfile(profile)
                    cl.sendText(msg.to,"名前を" + string + "に変更しました。")
#---------------------------------------------------------
            elif "ki名前変更:" in msg.text:
                string = msg.text.replace("ki名前変更:","")
                if len(string.decode('utf-8')) <= 20:
                    profile = ki.getProfile()
                    profile.displayName = string
                    ki.updateProfile(profile)
                    ki.sendText(msg.to,"名前を" + string + "に変更しました。")
#--------------------------------------------------------
            elif "ki2名前変更:" in msg.text:
                string = msg.text.replace("ki2名前変更:","")
                if len(string.decode('utf-8')) <= 20:
                    profile = ki2.getProfile()
                    profile.displayName = string
                    ki2.updateProfile(profile)
                    ki2.sendText(msg.to,"名前を" + string + "に変更しました。")
#--------------------------------------------------------
            elif "連絡先:" in msg.text:
                mmid = msg.text.replace("連絡先:","")
                msg.contentType = 13
                msg.contentMetadata = {"mid":mmid}
                cl.sendMessage(msg)
            elif msg.text in ["連絡先:on"]:
                if wait["contact"] == True:
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"既にオンです。")
                    else:
                        cl.sendText(msg.to,"是已经开。")
                else:
                    wait["contact"] = True
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"オンにしました。")
                    else:
                        cl.sendText(msg.to,"要了开。")
            elif msg.text in ["連絡先:off"]:
                if wait["contact"] == False:
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"既にオフです。")
                    else:
                        cl.sendText(msg.to,"是已经关断。")
                else:
                    wait["contact"] = False
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"オフにしました。")
                    else:
                        cl.sendText(msg.to,"要了关断。")
            elif msg.text in ["自動参加:on"]:
                if wait["autoJoin"] == True:
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"既にオンです。")
                    else:
                        cl.sendText(msg.to,"是已经开。")
                else:
                    wait["autoJoin"] = True
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"オンにしました。")
                    else:
                        cl.sendText(msg.to,"要了开。")
            elif msg.text in ["自動参加:off"]:
                if wait["autoJoin"] == False:
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"既にオフです。")
                    else:
                        cl.sendText(msg.to,"是已经关断。")
                else:
                    wait["autoJoin"] = False
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"オフにしました。")
                    else:
                        cl.sendText(msg.to,"要了关断。")
            elif "招待拒否:" in msg.text:
                try:
                    strnum = msg.text.replace("招待拒否:","")
                    if strnum == "オフ":
                        wait["autoCancel"]["on"] = False
                        if wait["lang"] == "JP":
                            cl.sendText(msg.to,"招待拒否をオフしました。\nオンにするときは人数を指定して送信して下さい。")
                        else:
                            cl.sendText(msg.to,"关了邀请拒绝。要时开请指定人数发送")
                    else:
                        num =  int(strnum)
                        wait["autoCancel"]["on"] = True
                        if wait["lang"] == "JP":
                            cl.sendText(msg.to,strnum + "人以下のグループは自動で招待拒否するようにしました。")
                        else:
                            cl.sendText(msg.to,strnum + "使人以下的小组用自动邀请拒绝")
                except:
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"値が間違っています。")
                    else:
                        cl.sendText(msg.to,"价值奇怪。")
            elif msg.text in ["強制on"]:
                if wait["leaveRoom"] == True:
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"既にオンです。")
                    else:
                        cl.sendText(msg.to,"是已经开。")
                else:
                    wait["leaveRoom"] = True
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"オンにしました。")
                    else:
                        cl.sendText(msg.to,"要了开。")
            elif msg.text in ["強制off"]:
                if wait["leaveRoom"] == False:
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"既にオフです。")
                    else:
                        cl.sendText(msg.to,"是已经关断。")
                else:
                    wait["leaveRoom"] = False
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"オフにしました。")
                    else:
                        cl.sendText(msg.to,"要了关断。")
            elif msg.text in ["共有on"]:
                if wait["timeline"] == True:
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"既にオンです。")
                    else:
                        cl.sendText(msg.to,"是已经开。")
                else:
                    wait["timeline"] = True
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"オンにしました。")
                    else:
                        cl.sendText(msg.to,"要了开。")
            elif msg.text in ["共有off"]:
                if wait["timeline"] == False:
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"既にオフです。")
                    else:
                        cl.sendText(msg.to,"是已经关断。")
                else:
                    wait["timeline"] = False
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"オフにしました。")
                    else:
                        cl.sendText(msg.to,"要了关断。")
            elif "Settings" == msg.text:
                md = ""
                if wait["contact"] == True: md+="連絡先有効\n"
                else: md+="連絡先無効\n"
                if wait["autoJoin"] == True: md+="自動参加有効\n"
                else: md +="自動参加無効\n"
                if wait["autoCancel"]["on"] == True:md+="招待拒否:" + str(wait["autoCancel"]["members"]) + "\n"
                else: md+= "招待拒否無効\n"
                if wait["leaveRoom"] == True: md+="強制自動退出有効\n"
                else: md+="強制自動退出無効\n"
                if wait["timeline"] == True: md+="共有有効\n"
                else:md+="共有無効\n"
                if wait["autoAdd"] == True: md+="自動追加有効\n"
                else:md+="自動追加無効\n"
                if wait["commentOn"] == True: md+="自動コメント有効\n"
                else:md+="自動コメント無効\n"
                cl.sendText(msg.to,md)
            elif "アルバム取得:" in msg.text:
                gid = msg.text.replace("アルバム取得:","")
                album = cl.getAlbum(gid)
                if album["result"]["items"] == []:
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"アルバムはありません。")
                    else:
                        cl.sendText(msg.to,"相册没在。")
                else:
                    if wait["lang"] == "JP":
                        mg = "以下が対象のアルバムです。"
                    else:
                        mg = "以下是对象的相册"
                    for y in album["result"]["items"]:
                        if "photoCount" in y:
                            mg += str(y["title"]) + ":" + str(y["photoCount"]) + "枚\n"
                        else:
                            mg += str(y["title"]) + ":0枚\n"
                    cl.sendText(msg.to,mg)
            elif "相簿→" in msg.text:
                gid = msg.text.replace("相簿→","")
                album = cl.getAlbum(gid)
                if album["result"]["items"] == []:
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"アルバムはありません。")
                    else:
                        cl.sendText(msg.to,"相册没在。")
                else:
                    if wait["lang"] == "JP":
                        mg = "以下が対象のアルバムです。"
                    else:
                        mg = "以下是对象的相册"
                    for y in album["result"]["items"]:
                        if "photoCount" in y:
                            mg += str(y["title"]) + ":" + str(y["photoCount"]) + "枚\n"
                        else:
                            mg += str(y["title"]) + ":0枚\n"
            elif "相簿刪除→" in msg.text:
                gid = msg.text.replace("相簿刪除→","")
                albums = cl.getAlbum(gid)["result"]["items"]
                i = 0
                if albums != []:
                    for album in albums:
                        cl.deleteAlbum(gid,album["id"])
                        i += 1
                if wait["lang"] == "JP":
                    cl.sendText(msg.to,str(i) + "件のアルバムを削除しました。")
                else:
                    cl.sendText(msg.to,str(i) + "删除了事的相册。")
            elif msg.text in ["参加グループid","群組全id"]:
                gid = cl.getGroupIdsJoined()
                g = ""
                for i in gid:
                    g += "[%s]:%s\n" % (cl.getGroup(i).name,i)
                cl.sendText(msg.to,g)
            elif msg.text in ["全招待拒否"]:
                gid = cl.getGroupIdsInvited()
                for i in gid:
                    cl.rejectGroupInvitation(i)
                if wait["lang"] == "JP":
                    cl.sendText(msg.to,"完了。")
                else:
                    cl.sendText(msg.to,"拒绝了全部的邀请。")
            elif "アルバム削除:" in msg.text:
                gid = msg.text.replace("アルバム削除:","")
                albums = cl.getAlbum(gid)["result"]["items"]
                i = 0
                if albums != []:
                    for album in albums:
                        cl.deleteAlbum(gid,album["id"])
                        i += 1
                if wait["lang"] == "JP":
                    cl.sendText(msg.to,str(i) + "件のアルバムを削除しました。")
                else:
                    cl.sendText(msg.to,str(i) + "删除了事的相册。")
            elif msg.text in ["追加:on"]:
                if wait["autoAdd"] == True:
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"既にオンです。")
                    else:
                        cl.sendText(msg.to,"是已经开。")
                else:
                    wait["autoAdd"] = True
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"オンにしました。")
                    else:
                        cl.sendText(msg.to,"要了开。")
            elif msg.text in ["追加:off"]:
                if wait["autoAdd"] == False:
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"既にオフです。")
                    else:
                        cl.sendText(msg.to,"是已经关断。")
                else:
                    wait["autoAdd"] = False
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"オフにしました。")
                    else:
                        cl.sendText(msg.to,"要了关断。")
            elif "自動追加メッセージ変更:" in msg.text:
                wait["message"] = msg.text.replace("自動追加メッセージ変更:","")
                cl.sendText(msg.to,"メッセージを変更しました。")
            elif "自動追加問候語變更→" in msg.text:
                wait["message"] = msg.text.replace("自動追加問候語變更→","")
                if wait["lang"] == "JP":
                    cl.sendText(msg.to,"メッセージを変更しました。")
                else:
                    cl.sendText(msg.to,"变更了信息。")
            elif msg.text in ["自動追加メッセージ確認","自動追加問候語確認"]:
                if wait["lang"] == "JP":
                    cl.sendText(msg.to,"自動追加メッセージは以下のように設定されています。\n\n" + wait["message"])
                else:
                    cl.sendText(msg.to,"自动追加信息像以下一样地被设定。\n\n" + wait["message"])
            elif msg.text in ["言語変更","言語變更"]:
                if wait["lang"] =="JP":
                    wait["lang"] = "TW"
                    cl.sendText(msg.to,"切換中國語。")
                else:
                    wait["lang"] = "JP"
                    cl.sendText(msg.to,"言語を日本語にしました。")
            elif "コメント変更→" in msg.text:
                c = msg.text.replace("コメント変更→","")
                if c in [""," ","\n",None]:
                    cl.sendText(msg.to,"変更できない文字列です。")
                else:
                    wait["comment"] = c
                    cl.sendText(msg.to,"変更しました。\n\n" + c)
            elif "留言設定:" in msg.text:
                c = msg.text.replace("留言設定:","")
                if c in [""," ","\n",None]:
                    cl.sendText(msg.to,"変更できない文字列です。")
                else:
                    wait["comment"] = c
                    cl.sendText(msg.to,"変更しました。\n\n" + c)
            elif msg.text in ["コメント有効","コメント：オン","コメント:on","自動首頁留言：開"]:
                if wait["commentOn"] == True:
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"既にオンです。")
                    else:
                        cl.sendText(msg.to,"是已经开。")
                else:
                    wait["commentOn"] = True
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"オンにしました。")
                    else:
                        cl.sendText(msg.to,"要了开。")
            elif msg.text in ["コメント無効","コメント：オフ","コメント:off","自動首頁留言：關"]:
                if wait["commentOn"] == False:
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"既にオフです。")
                    else:
                        cl.sendText(msg.to,"是已经关断。")
                else:
                    wait["commentOn"] = False
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"オフにしました。")
                    else:
                        cl.sendText(msg.to,"要了关断。")
            elif msg.text in ["コメント確認","留言確認"]:
                cl.sendText(msg.to,"現在自動コメントは以下のように設定されています。\n\n" + str(wait["comment"]))
            elif msg.text in ["url"]:
                if msg.toType == 2:
                    g = cl.getGroup(msg.to)
                    if g.preventJoinByTicket == True:
                        g.preventJoinByTicket = False
                        cl.updateGroup(g)
                    gurl = cl.reissueGroupTicket(msg.to)
                    cl.sendText(msg.to,"line://ti/g/" + gurl)
                else:
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"グループ以外では使用できません。")
                    else:
                        cl.sendText(msg.to,"以小组以外不能使用")
            elif "gurl:" in msg.text:
                if msg.toType == 2:
                    gid = msg.text.replace("gurl:","")
                    gurl = cl.reissueGroupTicket(gid)
                    cl.sendText(msg.to,"line://ti/g/" + gurl)
                else:
                    cl.sendText(msg.to,"グループ以外では使用できません。")
            
            elif "aurl:" in msg.text:
                if msg.toType == 1:
                    tid = msg.text.replace("aurl:","")
                    turl = ki.getUserTicket(tid)
                    ki.sendText(msg.to,"line://ti/p" + turl)
                else:
                    ki.sendText(msg.to,"error")

            elif "gurl得到→" in msg.text:
                if msg.toType == 2:
                    gid = msg.text.replace("gurl得到→","")
                    gurl = cl.reissueGroupTicket(gid)
                    cl.sendText(msg.to,"line://ti/g/" + gurl)
                else:
                    cl.sendText(msg.to,"以小组以外不能使用")
            elif msg.text in ["cb"]:
                wait["wblack"] = True
                cl.sendText(msg.to,"ブラックリストに追加する人の連絡先を送信してください。")
            elif msg.text in ["cbd"]:
                wait["dblack"] = True
                cl.sendText(msg.to,"ブラックリストから追加する人の連絡先を送信してください。")
            elif msg.text in ["cbc"]:
                if wait["commentBlack"] == {}:
                    cl.sendText(msg.to,"ブラックリストにしている人はいません。")
                else:
                    cl.sendText(msg.to,"以下がブラックリストです。")
                    mc = ""
                    for mi_d in wait["commentBlack"]:
                        mc += "・" +cl.getContact(mi_d).displayName + "\n"
                    cl.sendText(msg.to,mc)
            elif msg.text in ["名前時計有効"]:
                if wait["clock"] == True:
                    cl.sendText(msg.to,"既にオンです。")
                else:
                    wait["clock"] = True
                    now2 = datetime.now()
                    nowT = datetime.strftime(now2,"(%H:%M)")
                    profile = cl.getProfile()
                    profile.displayName = wait["cName"] + nowT
                    cl.updateProfile(profile)
                    cl.sendText(msg.to,"オンにしました。")
            elif msg.text in ["名前時計無効"]:
                if wait["clock"] == False:
                    cl.sendText(msg.to,"既にオフです。")
                else:
                    wait["clock"] = False
                    cl.sendText(msg.to,"オフにしました。")
            elif "名前時計変更:" in msg.text:
                n = msg.text.replace("名前時計変更:","")
                if len(n.decode("utf-8")) > 13:
                    cl.sendText(msg.to,"長すぎます。")
                else:
                    wait["cName"] = n
                    cl.sendText(msg.to,"変更しました。\n\n" + n)
            elif msg.text in ["時計更新"]:
                if wait["clock"] == True:
                    now2 = datetime.now()
                    nowT = datetime.strftime(now2,"(%H:%M)")
                    profile = cl.getProfile()
                    profile.displayName = wait["cName"] + nowT
                    cl.updateProfile(profile)
                    cl.sendText(msg.to,"更新しました。")
                else:
                    cl.sendText(msg.to,"名前時計をオンにしてください。")
            elif "NK:" in msg.text:
                if msg.toType == 2:
                    print "ok"
                    _name = msg.text.replace("NK:","")
                    gs = ki.getGroup(msg.to)
                    targets = []
                    for g in gs.members:
                        if _name in g.displayName:
                            targets.append(g.mid)
                    if targets == []:
                        ki.sendText(msg.to,"Not found.")
                    else:
                        for target in targets:
                            try:
                                klist=[ki,ki2,ki3,ki4,ki5,ki6,ki7,ki8,ki9,ki10,ki11,ki12,ki13]
                                kicker=random.choice(klist)
                                kicker.kickoutFromGroup(msg.to,[target])
                                print (msg.to,[g.mid])
                            except:
                                ki.sendText(msg.to,"Error")
#-----------------------------------------------------------
            elif "cki:" in msg.text:
                if msg.toType == 2:
                    print "ok"
                    _name = msg.text.replace("cki:","")
                    gs = cl.getGroup(msg.to)
                    targets = []
                    for g in gs.members:
                        if _name in g.displayName:
                            targets.append(g.mid)
                    if targets == []:
                        cl.sendText(msg.to,"Not found.")
                    else:
                        for target in targets:
                            try:
                                cl.kickoutFromGroup(msg.to,[target])
                                print (msg.to,[g.mid])
                            except:
                                pass
#-----------------------------------------------------------
            elif "kick:@" in msg.text:
                _name = msg.text.replace("kick:@","")
                _kicktarget = _name.rstrip(' ')
                gs = ki.getGroup(msg.to)
                targets = []
                for g in gs.members:
                    if _kicktarget == g.displayName:
                        targets.append(g.mid)
                        if targets == []:
                            cl.sendText(msg.to,"not found")
                        else:
                            for target in targets:
                                try:
                                    klist=[ki,ki2,ki3,ki4,ki5,ki6,ki7,ki8,ki9,ki10,ki11,ki12,ki13]
                                    kicker=random.choice(klist)
                                    kicker.kickoutFromGroup(msg.to,[target])
                                    print (msg.to,[g.mid])
                                except:
                                    ki.sendText(msg.to,"error")
#-----------------------------------------------------------
#statusMessage
            elif "SK:" in msg.text:
                if msg.toType == 2:
                    print "[SK]ok"
                    _name = msg.text.replace("SK:","")
                    gs = ki.getGroup(msg.to)
                    targets = []
                    for g in gs.members:
                        if _name in g.statusMessage:
                            targets.append(g.mid)
                    if targets == []:
                        ki.sendText(msg.to,"Not found.")
                    else:
                        for target in targets:
                            try:
                                klist=[ki,ki2,ki3,ki4,ki5,ki6,ki7,ki8,ki9,ki10,ki11,ki12,ki13]
                                kicker=random.choice(klist)
                                kicker.kickoutFromGroup(msg.to,[target])
                                print (msg.to,[g.mid])
                            except:
                                ki.sendText(msg.to,"Error")
#-----------------------------------------------------------



#-----------------------------------------------------------
            elif "KILL:@" in msg.text:
                _name = msg.text.replace("KILL:@","")
                _kicktarget = _name.rstrip(' ')
                gs = ki2.getGroup(msg.to)
                targets = []
                for g in gs.members:
                    if _kicktarget == g.displayName:
                        targets.append(g.mid)
                        if targets == []:
                            cl.sendText(msg.to,"not found")
                        else:
                            for target in targets:
                                try:
                                    wait["blacklist"][target] = True
                                    f=codecs.open('st2__b.json','w','utf-8')
                                    json.dump(wait["blacklist"], f, sort_keys=True, indent=4,ensure_ascii=False)
                                    ki2.sendText(msg.to,"ヽ( ^ω^)ﾉ ｻｸｾｽ！")
                                except:
                                    ki.sendText(msg.to,"error")
#-----------------------------------------------------------
            elif "midb:" in msg.text:
                midd = msg.text.replace("midb:","")
                wait["blacklist"][midd] = True
                f=codecs.open('st2__b.json','w','utf-8')
                json.dump(wait["blacklist"], f, sort_keys=True, indent=4,ensure_ascii=False)
#-----------------------------------------------------------
            elif "NB:" in msg.text:
                if msg.toType == 2:
                    print "[NB]ok"
                    _name = msg.text.replace("NB:","")
                    gs = ki.getGroup(msg.to)
                    targets = []
                    for g in gs.members:
                        if _name in g.displayName:
                            targets.append(g.mid)
                    if targets == []:
                        ki.sendText(msg.to,"Not found.")
                    else:
                        for target in targets:
                            try:
                                wait["blacklist"][target] = True
                                f=codecs.open('st2__b.json','w','utf-8')
                                json.dump(wait["blacklist"], f, sort_keys=True, indent=4,ensure_ascii=False)
                            except:
                                ki.sendText(msg.to,"Error")
#-----------------------------------------------------------
            elif "#終了" in msg.text:
                try:
                    import sys
                    sys.exit()
                except:
                    pass
#-----------------------------------------------------------

#-----------------------------------------------------------
            elif "☜( ՞ਊ ՞ )あああああああああああああああああああああああｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗ" in msg.text:
                ki.sendText(msg.to,"☜( ՞ਊ ՞ )あああああああああああああああああああああああｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗ")
                ki2.sendText(msg.to,"☜( ՞ਊ ՞ )あああああああああああああああああああああああｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗ")
#-----------------------------------------------------------speed
            elif msg.text in ["b"]:
                wait["wblacklist"] = True
                cl.sendText(msg.to,"ブラックリストに登録するアカウントを送信してください。")
            elif msg.text in ["bd"]:
                wait["dblacklist"] = True
                cl.sendText(msg.to,"ブラックリストから削除するアカウントを送信してください。")
            elif msg.text in ["bc"]:
                if wait["blacklist"] == {}:
                    cl.sendText(msg.to,"ブラックリストにしている人はいません。")
                else:
                    cl.sendText(msg.to,"以下がブラックリストです。")
                    mc = ""
                    for mi_d in wait["blacklist"]:
                        mc += "・" +cl.getContact(mi_d).displayName + "\n"
                    cl.sendText(msg.to,mc)
            elif msg.text in ["gbc"]:
                if msg.toType == 2:
                    group = cl.getGroup(msg.to)
                    gMembMids = [contact.mid for contact in group.members]
                    matched_list = []
                    for tag in wait["blacklist"]:
                        matched_list+=filter(lambda str: str == tag, gMembMids)
                    cocoa = ""
                    for mm in matched_list:
                        cocoa += "・" +cl.getContact(mm).displayName + "\n"
                    cl.sendText(msg.to,cocoa + "がブラックリストです。")
            elif msg.text in ["bk"]:
                if msg.toType == 2:
                    group = ki.getGroup(msg.to)
                    gMembMids = [contact.mid for contact in group.members]
                    matched_list = []
                    for tag in wait["blacklist"]:
                        matched_list+=filter(lambda str: str == tag, gMembMids)
                    if matched_list == []:
                        ki.sendText(msg.to,"ブラックリストユーザーはいませんでした。")
                        return
                    for jj in matched_list:
                        try:
                            klist=[ki,ki2,ki3,ki4,ki5,ki6,ki7,ki8,ki9]
                            kicker=random.choice(klist)
                            kicker.kickoutFromGroup(msg.to,[jj])
                            print (msg.to,[jj])
                        except:
                            pass
            elif msg.text in ["単蹴り"]:
                if msg.toType == 2:
                    group = cl.getGroup(msg.to)
                    gMembMids = [contact.mid for contact in group.invitee]
                    for _mid in gMembMids:
                        cl.cancelGroupInvitation(msg.to,[_mid])
                    cl.sendText(msg.to,"と見せかけてキャンセルしました。")
            elif "random:" in msg.text:
                if msg.toType == 2:
                    strnum = msg.text.replace("random:","")
                    source_str = 'abcdefghijklmnopqrstuvwxyz1234567890@:;./_][!&%$#)(=~^|'
                    try:
                        num = int(strnum)
                        group = cl.getGroup(msg.to)
                        for var in range(0,num):
                            name = "".join([random.choice(source_str) for x in xrange(10)])
                            time.sleep(0.01)
                            group.name = name
                            cl.updateGroup(group)
                    except:
                        cl.sendText(msg.to,"Error")
            elif "アルバム作成:" in msg.text:
                try:
                    albumtags = msg.text.replace("アルバム作成:","")
                    gid = albumtags[:33]
                    name = albumtags.replace(albumtags[:34],"")
                    cl.createAlbum(gid,name)
                    cl.sendText(msg.to,name + "アルバムを作成しました。")
                except:
                    cl.sendText(msg.to,"Error")
            elif "fakec→" in msg.text:
                try:
                    source_str = 'abcdefghijklmnopqrstuvwxyz1234567890@:;./_][!&%$#)(=~^|'
                    name = "".join([random.choice(source_str) for x in xrange(10)])
                    amid = msg.text.replace("fakec→","")
                    cl.sendText(msg.to,str(cl.channel.createAlbumF(msg.to,name,amid)))
                except Exception as e:
                    try:
                        cl.sendText(msg.to,str(e))
                    except:
                        pass

#-----------------------------------------------

#-----------------------------------------------

            elif "join" in msg.text:
                        G = cl.getGroup(msg.to)
                        ginfo = cl.getGroup(msg.to)
                        G.preventJoinByTicket = False
                        cl.updateGroup(G)
                        invsend = 0
                        Ticket = cl.reissueGroupTicket(msg.to)
                        ki.acceptGroupInvitationByTicket(msg.to,Ticket)
                        time.sleep(0.1)
                        ki2.acceptGroupInvitationByTicket(msg.to,Ticket)
                        time.sleep(0.1)
                        ki.sendText(msg.to,"[" + str(ginfo.name) + "]\n\n" + "にkickerが参加しました")
                        print "kicker ok"
                        G.preventJoinByTicket =True
                        ki.updateGroup(G)
                       
#-----------------------------------------------
            elif "kicker" in msg.text:
                        G = cl.getGroup(msg.to)
                        ginfo = cl.getGroup(msg.to)
                        G.preventJoinByTicket = False
                        cl.updateGroup(G)
                        invsend = 0
                        Ticket = cl.reissueGroupTicket(msg.to)
                        ki.acceptGroupInvitationByTicket(msg.to,Ticket)
                        ki2.acceptGroupInvitationByTicket(msg.to,Ticket)
                        print "kicker ok"
                        G.preventJoinByTicket = True
                        cl.updateGroup(G)
#-----------------------------------------------
            elif "leave" in msg.text:
                if msg.toType == 2:
                    ginfo = cl.getGroup(msg.to)
                    try:
                        ki.leaveGroup(msg.to)
                        ki2.leaveGroup(msg.to)
                    except:
                        pass
#-----------------------------------------------
            elif "#test" in msg.text:
                ki.sendText(msg.to,"ok")
                ki2.sendText(msg.to,"ok")
#----------------------------------------------- 
#-----------------------------------------------

            elif "speed" in msg.text:
                start = time.time()
                cl.sendText(msg.to, "計測中です...")
                elapsed_time = time.time() - start
                cl.sendText(msg.to, "%s秒" % (elapsed_time))

#-------------------------------------------------------------------蹴り返し
        if op.type == 19:
            try:
                if op.param3 in mid:
                    if op.param2 in kimid:
                        G = ki.getGroup(op.param1)
                        G.preventJoinByTicket = False
                        ki.updateGroup(G)
                        Ticket = ki.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        ki.updateGroup(G)
                    else:
                        G = ki.getGroup(op.param1)

                        cl.kickoutFromGroup(op.param1,[op.param2])

                        G.preventJoinByTicket = False
                        ki.updateGroup(G)
                        Ticket = ki.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        ki.updateGroup(G)
                        wait["blacklist"][op.param2] = True

                       
                elif op.param3 in kimid:
                    if op.param2 in mid:
                        G = cl.getGroup(op.param1)
                        G.preventJoinByTicket = False
                        cl.updateGroup(G)
                        Ticket = cl.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        cl.updateGroup(G)
                    else:
                        G = cl.getGroup(op.param1)

                        ki.kickoutFromGroup(op.param1,[op.param2])

                        G.preventJoinByTicket = False
                        cl.updateGroup(G)
                        Ticket = cl.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        cl.updateGroup(G)

                        wait["blacklist"][op.param2] = True


                elif op.param3 in k2mid:
                    if op.param2 in kimid:
                        G = ki.getGroup(op.param1)
                        G.preventJoinByTicket = False
                        ki.updateGroup(G)
                        Ticket = ki.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        ki.updateGroup(G)
                    else:
                        G = ki2.getGroup(op.param1)

                        ki.kickoutFromGroup(op.param1,[op.param2])

                        G.preventJoinByTicket = False
                        ki.updateGroup(G)
                        Ticket = ki2.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        ki.updateGroup(G)
                
            except:
                pass
#------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------
        if op.type == 59:
            print op


    except Exception as error:
        print error


def a2():
    now2 = datetime.now()
    nowT = datetime.strftime(now2,"%M")
    if nowT[14:] in ["10","20","30","40","50","00"]:
        return False
    else:
        return True
def nameUpdate():
    while True:
        try:
        #while a2():
            #pass
            if wait["clock"] == True:
                now2 = datetime.now()
                nowT = datetime.strftime(now2,"(%H:%M)")
                profile = cl.getProfile()
                profile.displayName = wait["cName"] + nowT
                cl.updateProfile(profile)
            time.sleep(600)
        except:
            pass
#----------------------------------------

#-------------------------------
thread2 = threading.Thread(target=nameUpdate)
thread2.daemon = True
thread2.start()

while True:
    bot(cl.Poll.stream(50000))

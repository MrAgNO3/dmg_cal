from PySide6.QtWidgets import *
from PySide6.QtUiTools import *
from PySide6.QtGui import QIcon
from math import *
import json
app = QApplication()
# 加载ui和logo
app.setWindowIcon(QIcon('logo.png'))
ui = QUiLoader().load('dmg_cal.ui')
rS = True

def myEval(cont,value = 0):
    '''
    如果发生错误则返回value，否则eval返回的结果
    '''
    if cont == '':
        return value
    return eval(cont)


def Save():
    data = {
        'atk': ui.atk.text(),
        'tal': ui.talent.text(),
        'dmgBuff': ui.dmgBuff.text(),
        'cRate': ui.crit_rate.text(),
        'cDmg': ui.crit_dmg.text(),
        'buff': ui.buff.text(),
        'resis': ui.resistance.text(),
        'l1': int(ui.char_level.text()),
        'l2': int(ui.mons_level.text()),
        'def': ui.defense.text(),
        'em': ui.Elem_mas.text(),
        'emBuff': ui.em_buff.text(),
        'reactBuff': ui.reactBuff.text(),
        'react': {'无倍率反应':0,'1.5倍率反应':1,'2倍率反应':2}[ui.buttonGroup.checkedButton().text()],
        'emBuffType' : {'元素精通':0,'反应伤害提升':1}[ui.buttonGroup_2.checkedButton().text()]
        }
    with open('data.json','w') as f:
        json.dump(data,f)
        ui.res.setText('Data saved')


def Load():
    with open('data.json') as f:
        data = json.load(f)
    ui.atk.setText(data['atk'])
    ui.talent.setText(data['tal'])
    ui.dmgBuff.setText(data['dmgBuff'])
    ui.crit_rate.setText(data['cRate'])
    ui.crit_dmg.setText(data['cDmg'])
    ui.buff.setText(data['buff'])
    ui.resistance.setText(data['resis'])
    ui.defense.setText(data['def'])
    ui.Elem_mas.setText(data['em'])
    ui.em_buff.setText(data['emBuff'])
    ui.reactBuff.setText(data['reactBuff'])
    ui.buttonGroup.buttons()[data['react']].setChecked(True)
    ui.buttonGroup_2.buttons()[data['emBuffType']].setChecked(True)
    ui.char_level.setValue(data['l1'])
    ui.mons_level.setValue(data['l2'])
    ui.res.setText('Data loaded')
    

def Clear():
    for i in dir(ui):
        if type(getattr(ui,i)) == type(ui.atk):
            getattr(ui,i).setText('')
    ui.char_level.setValue(90)
    ui.mons_level.setValue(90)
    ui.res.setText('')

def func():
    
    ans,err,flag = '','',False

    try:
        att = myEval(ui.atk.text(),1000)
        ans += f'攻击力:{att}\n'
    except Exception as e:
        flag = True
        err += f'Atk wrong, {e} \n'


    try:
        tal = myEval(ui.talent.text(),100)
        ans += '技能倍率:'+'{:.1f}'.format(tal)+'%  \n'
    except Exception as e:
        flag = True
        err += f'Talent wrong,{e}\n'


    try:
        dmgBuff = myEval(ui.dmgBuff.text(),0)
        if dmgBuff != 0:
            ans += f'伤害提高:{dmgBuff}\n'
    except Exception as e:
        flag = True
        err += f'Damage boost wrong,{e}\n'

        
    try:
        # 暴击率只计算小于 100% 的部分
        crate = myEval(ui.crit_rate.text(),5)
        ans += '暴击率:'+'{:.1f}'.format(crate)+'%  '
        crate = max(min(crate,100),0)
    except Exception as e:
        flag = True
        err += f'CRIT rate wrong, {e}\n'


    try:
        # 未考虑爆伤为负的情况
        cdmg = myEval(ui.crit_dmg.text(),50)
        ans += '暴伤:'+'{:.1f}'.format(cdmg)+'%  \n'
    except Exception as e:
        flag = True
        err += f'CRIT DMG wrong, {e} \n'


    try:
        buff = myEval(ui.buff.text())
        ans += '伤害加成:'+'{:.1f}'.format(buff)+'%  \n'
    except Exception as e:
        flag = True
        err += f'Buff wrong, {e} \n'


    try:
        resis = myEval(ui.resistance.text(),10)
        ans += f'怪物抗性:{resis}%\n'
    except Exception as e:
        flag = True
        err += f'Resistance wrong, {e}\n'
    # https://nga.178.com/read.php?tid=24079044
    # 抗性系数
    if resis >= 75:
        t_resis = 1/(resis/25 + 1)
    elif resis >= 0:
        t_resis = 1-resis/100
    else:
        t_resis = 1-resis/200

    
    try:
        # https://www.bilibili.com/read/cv10004413/
        # 等级/防御系数
        l1, l2 = int(ui.char_level.text()), int(ui.mons_level.text())
        l1 = max(1,min(l1,90))
        l2 = max(1,l2)
        anti_def = myEval(ui.defense.text())
        t_def = (100 + l1)/(100 + l1 + (100+l2)*(1-anti_def/100))
    except Exception as e:
        err += f'Level wrong, {e}\n'
        flag = True

    react = ui.buttonGroup.checkedButton().text()
    if react == '无倍率反应':
        t_react = 1
    elif react == '1.5倍率反应':
        t_react = 1.5
    elif react == '2倍率反应':
        t_react = 2
    
    try:
        if t_react != 1:
            # 若选择了无倍率反应，则跳过这一步
            
            if ui.EM_btn.isChecked():
                # 使用元素精通
                em = myEval(ui.Elem_mas.text())
                em_buff = 0 if em == 0 else (6.665-9340/(em+1401))/2.4
                ans += f'元素精通:{em}\t'
                
            elif ui.EMbuff_btn.isChecked():
                # 直接使用加成数值
                em_buff = myEval(ui.em_buff.text())/100

            reactBuff = myEval(ui.reactBuff.text())
            if reactBuff != 0:
                em_buff += reactBuff/100
                ans += '增幅反应增伤:{:.2f}% + {}%\n'.format(em_buff*100,reactBuff)
            else:
                ans += '增幅反应增伤:{:.2f}%'.format(em_buff*100)
            t_react *= em_buff+1
                
    except Exception as e:
        flag = True
        err += f'Element master wrong, {e}\n'
            
    if not flag:#  and att > 0 and crate >= 0 and cdmg > 0 and buff >= 0 and tal > 0 and elemas >= 0 and resis <= 100:
        t = t_react * t_def * t_resis
        # 暴击伤害
        critDmg = (att * tal/100 + dmgBuff) * (1+cdmg/100) * (1+buff/100)  * t
        # 不暴击伤害
        noCritDmg = (att * tal/100 + dmgBuff)* (1+buff/100) * t
        # 伤害期望
        Edmg = (att * tal/100 + dmgBuff) * (1+crate/100*cdmg/100) * (1+buff/100) * t
        
        
        ans += f'''
            伤害期望: {round(Edmg)}
            不暴击伤害: {round(noCritDmg)}
            暴击伤害: {round(critDmg)}
        '''
        # ans += '\n总伤害期望:'+str(round(Edmg*t))+'\n'
        # ans += f'单次不暴击伤害:{round(SingleDmg*t/(1+cdmg/100))}\n'
        # ans += '单次暴击伤害:'+str(round(SingleDmg*t))+'\n'
        ui.res.setText(ans)
    else:
        err += 'Illegal Data.'
        ans = ' \n请输入正确格式数据'
        ui.res.setText(err+ans)


def func1():
    print()
    ui.ra150.setChecked(True)
    # ui.nora.setChecked(True)
    pass

ui.cal.clicked.connect(func)
# ui.cal.clicked.connect(func1)
ui.saveBtn.clicked.connect(Save)
ui.loadBtn.clicked.connect(Load)
ui.clearBtn.clicked.connect(Clear)
ui.show()
if ui.autoSave.isChecked():
    Load()
app.exec()
if ui.autoSave.isChecked():
    Save()
    


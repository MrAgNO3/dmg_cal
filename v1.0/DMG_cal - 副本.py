from PySide2.QtWidgets import *
from PySide2.QtUiTools import *
from PySide2.QtGui import  QIcon
from math import *

app = QApplication([])
app.setWindowIcon(QIcon('logo.png'))
ui = QUiLoader().load('dmg_cal.ui')
def func():
    ans,err,flag = '','',False
    att,crate,cdmg,buff,tal,resis,t,l1,l2,elemas = 0,0,50,0,0,10,1,90,90,0
    
    try:
        att = int(eval(ui.atk.text()))
        ans += '攻击力:'+str(att)+'  '
    except:
        flag = True
        err += 'Atk wrong,'
        
    try:
        crate = eval(ui.crit_rate.text())
        ans += '暴击率:'+'{:.1f}'.format(crate)+'%  '
    except:
        if ui.crit_rate.text() == '':
            crate = 0
            ans += '暴击率:'+'{:.1f}'.format(crate)+'%  '
        else:
            flag = True
            err += 'CRIT rate wrong,'

    try:
        cdmg = eval(ui.crit_dmg.text())
        ans += '\n暴击伤害:'+'{:.1f}'.format(cdmg)+'%  '
    except:
        if ui.crit_dmg.text() == '':
            crate = 50
            ans += '\n暴击伤害:'+'{:.1f}'.format(crate)+'%  '
        else:
            flag = True
            err += 'CRIT DMG wrong,'

    try:
        buff = eval(ui.buff.text())
        ans += '伤害加成:'+'{:.1f}'.format(buff)+'%  \n'
    except:
        if ui.buff.text() == '':
            buff = 0
            ans += '伤害加成:'+'{:.1f}'.format(buff)+'%  \n'
        else:
            flag = True
            err += 'Buff wrong,'
    
    try:
        tal = eval(ui.talent.text())
        ans += '技能倍率:'+'{:.1f}'.format(tal)+'%  '
    except:
        flag = True
        err += 'Talent wrong,'

    try:
        resis = eval(ui.resistance.text())
        ans += '怪物抗性:'+'{:.1f}'.format(resis)+'%  '
    except:
        if ui.resistance.text() == '':
            resis = 10
            ans += '怪物抗性:'+'{:.1f}'.format(resis)+'%  \n'
        else:
            flag = True
            err += 'Resistance wrong,'
    if resis >= 0:t = 1-resis/100
    else:t = 1-resis/200

    l1,l2 = int(ui.char_level.text()),int(ui.mons_level.text())
    if l1 != 0 and l2 != 0:
        t *= (100+l1)/(200+l1+l2)
    elif l1 == 0 and l2 == 0:
        pass
    else:
        err += 'Level wrong, '
        flag = True

    react = ui.buttonGroup.checkedButton().text()
    if react == '无倍率反应':pass
    else:
        if react == '1.5倍率反应':t *= 1.5
        elif react == '2倍率反应': t *= 2
        try:
            elemas = eval(ui.Elem_mas.text())
            ans += '元素精通增伤:{:.1f}\n'.format(elemas)
            t *= (1+elemas/100)
        except:
            if ui.Elem_mas.text() == '':
                elemas = 0
                ans += '元素精通增伤:{:.1f}\n'.format(elemas)
            else:
                flag = True
                err += 'Element master wrong, '
            
    if not flag and att > 0 and crate>=0 and cdmg>0 and buff>=0 and tal>0 and elemas >= 0:
        Edmg = att*(1+crate/100*cdmg/100)*(1+buff/100)*tal/100
        SingleDmg = att*(1+cdmg/100)*(1+buff/100)*tal/100
        ans += '\n伤害期望:'+str(round(Edmg*t))+'\n'
        if crate == 0:ans += '单次暴击伤害:暴击率为0，不会暴击'
        else:ans += '单次暴击伤害:'+str(round(SingleDmg*t))+'\n'
        ui.res.setText(ans)
    else:
        err += 'Illegal Data.'
        ans = ' \n请输入正确格式数据'
        ui.res.setText(err+ans)
ui.cal.clicked.connect(func)
ui.show()
app.exec_()

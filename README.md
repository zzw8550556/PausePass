# PausePass
本脚本配合安卓手机应用锁，可以实现真正的app冷静期  

有时候在手机上刷一个app上瘾，就需要使用手机的应用锁来设置密码来防止自己再玩。  

但应用锁的密码如果是自己记得的常用密码，那么上瘾的时候很容易管不住自己解锁，这样的应用锁就形同虚设。  

如果能够生成一个自己陌生的密码，只显示一次，在设定的冷静期之后显示密码，就可以实现真正的应用冷静期。  

本脚本实现的功能就是：  
生成密码但只显示一次，在冷静期之后延时显示密码。  
在显示一次密码之后的一段时间内，密码仅保存在内存中，没有其他办法获取到密码，在一段时间结束后，将密码保存在文件中，并可以通过脚本读取。  

##使用：
### 1.安装库文件
pip install cryptography
pip install readchar
### 2.生成盐
python salt_generate.py 会在本目录下生成 'salt.pkl' 文件，用于保存盐
python salt_display.py 生成 'salt.pkl' 文件后，运行可以显示盐的内容
### 3.运行
python key_generate.py 会显示生成的密码，按回车后密码不再显示，程序运行一天后，会在本目录下生成 'key.pkl' 文件，密码保存在里面
        当按回车后密码不再显示之后，为防止紧急情况，当按ctrl+c退出程序时，会立即在本目录下生成 'key.pkl' 文件，密码保存在里面
python key_display.py 生成 'key.pkl' 文件后，运行可以显示密码的内容，注意显示密码需要口令，口令为'pwd123'

##提示
在程序执行期间，密码仅被储存在内存中，不存在其他正常途径能够获取该密码。请您谨慎操作，并理解使用此工具所可能带来的风险。任何由此产生的后果，本项目概不负责。

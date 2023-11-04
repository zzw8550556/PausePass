# PausePass
本脚本配合安卓手机应用锁，可以实现真正的app冷静期  
有时候在手机上刷一个app上瘾，就需要使用手机的应用锁来设置密码来防止自己再玩。  
但应用锁的密码如果是自己记得的常用密码，那么上瘾的时候很容易管不住自己解锁，这样的应用锁就形同虚设。  
如果能够生成一个自己陌生的密码，只显示一次，在设定的冷静期之后显示密码，就可以实现真正的应用冷静期。  
本脚本实现的功能就是：  
生成密码但只显示一次，在冷静期之后延时显示密码。  
在显示一次密码之后的一段时间内，密码仅保存在内存中，没有其他办法获取到密码，在一段时间结束后，将密码保存在文件中，并可以通过脚本读取。  

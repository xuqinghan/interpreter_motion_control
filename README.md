# interpreter_motion_control

1 解释性脚本语言： 因为需要单步运行跟踪。不适合编译

    也便于用 GOTO 实现 LOOP

2 最多 最外层1层LOOP 因为没有条件返回

3 需要内置1个 RESET ALL  复位所有的东西到初始状态！

4 注释占1行

5 单步时，记录有效行号（跳过注释和空白行）

6 GOTO维护 程序指针

程序解释为中间指令：

[1 LABEL A
2 MOVE para1,...
4 MOVE para1,...
7 GOTO 1
]

实际执行时： ptr移动




# 需要沙盘厂家定义的：

config.py中
1 camera 的4方向 对应的 cXdX
2 RESET_ALL 宏 全部东西复位的指令集合（每个轨道的初始位置，应该不是停在轨道中间）



# 用户编程语句指令手册 User Programming Manual

## 1 舰船别名定义
    用户在程序段首 给b1 - b7 船只 起别名，用于舰船移动指令
    全局1段
    格式 
        BEG DEFINE
            b1 别名1
            b2 别名2
            ......
        END DEFINE

## 2 程序体
    需要执行的语句块，全局一段
    类似html中的<body></body>
    格式
        BEG BODY
            语句1
            语句2
            ......
        END BODY

## 3 舰船移动
    格式
        自然选择 前进/后退 3
## 4 相机指令
    -  4.1 移动
        格式  
            CAMERA ↑/↓/←/→ 速度
    -  4.2 停止
        格式
            CAMERA STOP
    -  4.3 拍照
        格式
            CAMERA SNAPSHOT            
## 5 定时指令
    用来等待移动一段时间
    格式
        WAIT 秒数
## 6 LOOP
    全局目前只能实现1个循环，且不会自动停止，没有条件判断语句，无法退出，需要手动打断
    格式
        BEG LOOP
            语句1
            语句2
            ......
        END LOOP        

## 7 全体复位
    相机、全部的船只复位
    格式
        RESET ALL

## 8 注释
    用户注释，占1行 “#”开头
    格式
        # 注释内容

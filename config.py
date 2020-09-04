#相机在2个轴上移动  v0 停止
camera = {
    'MOVE': {
        # 相机 2个轴 需要结合电机实际调整
        '↑': 'c1d1',
        '↓': 'c1d2',
        '←': 'c2d1',
        '→': 'c2d2',
    },
    'STOP': ['c1d0v0', 'c2d0v0'], #同时停止2个轴
    'velocity': 3, #速度有3级 1-3级
}

line = {
    'object': ['b1', 'b2', 'b3', 'b4'],
    'direct': {'前进': 1, '后退': 2},
    'STOP': 'd0v0',
    'velocity': 3, #速度有3级
}

circle = {
    'object': ['b5', 'b6', 'b7'],
    'direct': {'前进': 1}, #只有1个方向
    'velocity': 3, #速度有3级
    'STOP': 'd0v0',
}

#复位= 全部电机以最快速度 向初始方向移动 + WAIT 一定时间
#需要出厂前定义 测试
reset_all = {
    'MOVE': [
        'c1d1v3',
        'c2d1v3',
        'b1d1v3',
        'b2d1v3',  
        'b3d1v3',
        'b4d1v3',
        'b5d1v3',
        'b6d1v3',
        'b7d1v3',
    ],
    'SEC_ALL_OVER': 5, #全部东西复位完成的秒数，通过实测确定 
}

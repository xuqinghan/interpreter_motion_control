'''
    分为编译时和运行时
    编译时 编译有效语句为IL语言，记录行号 到CMD_LINE
    运行时 维护当前程序指针 运行CMD_LINE
'''

import u_comm
import time
import config

#---------------compile-----------------------


def parse_DEFINE(lines_plan):
    begin = False
    object_dict = {}
    for line in lines_plan:
        if line[0] == '#':
            continue
        if line == 'BEG DEFINE':
            begin = True
            continue
        elif line == 'END DEFINE':
            break

        if begin:
            object_name, object_alias, *_ = line.split(' ')

            object_dict[object_alias] = object_name

    #转dict
    return object_dict

def parse_move_object1(object_str, words, config_type):
    '''1行移动'''
    #转换为 bX
    if 'STOP' == words[1]:
        command1 = lambda : u_comm.send1(f'{object_str}{direct}')
    else:

        velocity = int(words[2])
        assert words[1] in config_type['direct']
        direct = config_type['direct'][words[1]]
        assert velocity >=0 and velocity <= config_type['velocity'] 
        #object_str, direct, velocity
        command1 = ('MOVE', f'{object_str}d{direct}v{velocity}')
    return command1

def parse_command1(line1, object_dict):
    '''解释一条简单指令 成若干行 IL指令 
        因为要GOTO
        1行IL 保存为tuple
        多行IL 保存为list(tuple)
    '''
    words = line1.split(' ')
    #print(words)
    if words[0] == 'WAIT':
        sec = float(words[1])
        command1 = ('WAIT', sec)
    elif words[0] == 'CAMERA':
        #相机
        action = words[1]
        if action == 'MOVE':
            #移动
            #CAMERA MOVE ↑ 1
            #包含c1 c2
            
            velocity = int(words[3])
            assert words[2] in config.camera['MOVE']
            direct = config.camera['MOVE'][words[2]]
            assert velocity >=0 and velocity <= config.camera['velocity']            
            command1 = ('MOVE', f'{direct}v{velocity}')
        elif action == 'STOP':
            #STOP 直接执行2条指令
            command1 = [('MOVE', line) for line in config.camera['STOP']]
    elif words[0] in object_dict:
        object_str = object_dict[words[0]]
        if object_str in config.line['object']:
            #直线移动物体
            command1 = parse_move_object1(object_str, words, config.line)
        elif object_str in config.circle['object']:
            #环形移动物体
            command1 = parse_move_object1(object_str, words, config.circle)
    elif line1 == 'BEG LOOP':
        #需要GOTO到 编译行号中 最近的的'BEG LOOP'行
        command1 = ('LABEL', line1)
    elif line1 == 'END LOOP':
        #需要GOTO到 最近的 'BEG LOOP'
        command1 = ('GOTO', 'BEG LOOP')
    elif line1 == 'RESET ALL':
        #复位所有的
        lines_IL_MOVE = [('MOVE', il) for il in config.reset_all['MOVE']]
        IL_wait = ('WAIT', config.reset_all['SEC_ALL_OVER'])
        command1 = [*lines_IL_MOVE, IL_wait]
    else:
        #任何其他指令，注释行，空白行 当成无效指令
        command1 = None

    return command1


def parse_BODY(lines_plan, object_dict):
    '''全部BODY内的行，记录行号'''
    begin = False
    commands = []
    for num_line, line1 in enumerate(lines_plan):
        if line1 == 'BEG BODY':
            begin = True
            continue
        elif line1 == 'END BODY':
            break

        if begin:
            IL_line1 = parse_command1(line1, object_dict)
            #原行号，解释后的中间语言
            commands.append((num_line, IL_line1))
    return commands

def compile_time(lines_plan_in:list):
    #过滤掉每行前后空格
    lines_plan = [line for line in lines_plan_in if line.strip()]
    #不过滤空行和注释行 因为行号仍然保留
    #lines_plan = [line for line in lines_plan_in if line[0] != '#']
    # DEFINE字段 
    object_dict = parse_DEFINE(lines_plan)
    # BODY 字段
    CMDS_LINES = parse_BODY(lines_plan, object_dict)
    return CMDS_LINES
#--------------runtime--------------------------

def run_time(CMDS_LINES, is_step=False):
    '''在中间语言上执行 RESET ALL CAMERA STOP 可能被解释成多行[]'''
    current_ptr = 0
    #LABEL对应的指针
    LABEL_prt_dict = {}

    def run_IL_line1(IL_line1):
        nonlocal current_ptr
        CMD, *para = IL_line1
        if CMD == 'GOTO':
            #参数是label 
            current_ptr = LABEL_prt_dict[para[0]]
            print(f'GOTO {CMDS_LINES[current_ptr]}')
        elif CMD == 'LABEL':
            #参数是label
            LABEL_prt_dict[para[0]] = current_ptr
            print('LABEL')
        elif CMD == 'MOVE':
            u_comm.send1(para[0])
        elif CMD == 'WAIT':
            print(f'等待 {para[0]} 秒')
            time.sleep(para[0])
        else:
            raise Exception(f"invalid IL {CMD}")

    while current_ptr < len(CMDS_LINES):
        num_line1, CMD_LINE1 = CMDS_LINES[current_ptr]
        print(f'准备执行执行第{num_line1}行')
        #发送通知GUI高亮当前行
        #单步在这里等待玩家指令
        if is_step:
            wait_step = False
            while True:
                if wait_step:
                    break

        #单步确认，继续执行
        if isinstance(CMD_LINE1, list):
            #如果是多行
            for IL_line1 in CMD_LINE1:
                run_IL_line1(IL_line1)
        elif isinstance(CMD_LINE1, tuple):
            #单行
            run_IL_line1(CMD_LINE1)
        
        current_ptr += 1

    print('执行完毕')
    #通知GUI 熄灭全部行，按钮复位


def test_call():
    command1 = lambda : print('哈哈')
    command1.__call__()

if __name__ == '__main__':
    #读取
    with open('./mock/plan1.txt', 'r',  encoding= 'UTF-8') as f:
        lines_plan = f.readlines()

    is_step = False
    #编译
    lines_plan = [line.strip(' \n') for line in lines_plan ]
    #print(lines_plan)
    #不过滤空行和注释行 因为行号仍然保留
    #lines_plan = [line for line in lines_plan_in if line[0] != '#']
    # DEFINE字段 
    # object_dict = parse_DEFINE(lines_plan)
    # print(object_dict)
    # # BODY 字段
    # print(object_dict)
    # CMDS_LINES = parse_BODY(lines_plan, object_dict)
    CMDS_LINES = compile_time(lines_plan)
    print('编译后中间语言', CMDS_LINES)
    #运行
    run_time(CMDS_LINES, is_step)
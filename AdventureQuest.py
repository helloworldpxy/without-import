# 文字冒险游戏
class Room:
    def __init__(self, name, description, exits=None, items=None, enemies=None):
        self.name = name
        self.description = description
        self.exits = exits if exits is not None else {}
        self.items = items if items is not None else []
        self.enemies = enemies if enemies is not None else []

class Player:
    def __init__(self):
        self.current_room = None
        self.inventory = []
        self.health = 100

class Enemy:
    def __init__(self, name, health, strength, description):
        self.name = name
        self.health = health
        self.strength = strength
        self.description = description

def create_world():
    try:
        # 初始化房间
        start = Room("Start Room", 
                     "石墙潮湿发亮，北方有扇锈迹斑斑的铁门。你手中握着一把生锈的钥匙。",
                     {"north": hallway}, ["rusty_key"], [])
        
        hallway = Room("Dark Hallway",
                       "昏暗的走廊延伸向北，南方是来路。墙上挂着空剑鞘。",
                       {"north": guard_room, "south": start}, ["sword_sheath"], [])
        
        treasure = Room("Treasure Chamber",
                        "金光闪耀！宝箱中央立着王座，但被锁链束缚着钻石王冠。",
                        {"south": guard_room}, ["diamond_crown"], [])
        
        guard_room = Room("Guard Room",
                          "一个守卫站在这里，守卫着通向宝藏室的门。",
                          {"north": treasure, "south": hallway}, ["gold_coin"], 
                          [Enemy("Guard", 50, 10, "一个强壮的守卫，手持长剑。")])
        
        return [start, hallway, guard_room, treasure]
    except Exception as e:
        print(f"创建世界时发生错误: {e}")
        return []

def parse_input():
    try:
        raw = input("\n> ").strip().lower()
        parts = raw.split()
        verb = parts[0] if parts else ""
        noun = parts[1] if len(parts) > 1 else ""
        return verb, noun
    except Exception as e:
        print(f"处理输入时发生错误: {e}")
        return "", ""

def combat(player, enemy):
    try:
        while player.health > 0 and enemy.health > 0:
            print(f"\n战斗中: {enemy.name}")
            print(enemy.description)
            action = input("你想做什么？(攻击/逃跑)\n> ").strip().lower()
            if action == "攻击":
                enemy.health -= 10
                print(f"你攻击了{enemy.name}，他的生命值现在是{enemy.health}/100")
                if enemy.health > 0:
                    player.health -= enemy.strength
                    print(f"{enemy.name}反击了你，你的生命值现在是{player.health}/100")
            elif action == "逃跑":
                print("你试图逃跑，但敌人拦住了你！")
            else:
                print("未知命令。")
            
        if enemy.health <= 0:
            print(f"\n你击败了{enemy.name}！")
            return True
        else:
            print("\n你被击败了...")
            return False
    except Exception as e:
        print(f"战斗过程中发生错误: {e}")
        return False

def main():
    world = create_world()
    if not world:
        print("游戏无法开始，世界未正确创建。")
        return
    
    player = Player()
    player.current_room = world[0]
    
    print("=== 冒险游戏 ===\n输入 'help' 查看命令")
    
    while True:
        try:
            # 显示当前状态
            print(f"\n{player.current_room.name}")
            print(player.current_room.description)
            
            if player.current_room.items:
                print(f"可见物品: {', '.join(player.current_room.items)}")
            
            if player.current_room.enemies:
                print(f"可见敌人: {', '.join([enemy.name for enemy in player.current_room.enemies])}")
            
            if player.health < 100:
                print(f"生命值: {player.health}/100")
            
            # 处理输入
            verb, noun = parse_input()
            
            # 命令处理逻辑
            if verb == "go":
                if noun in player.current_room.exits:
                    player.current_room = player.current_room.exits[noun]
                else:
                    print("无法往那个方向移动。")
                    
            elif verb == "take":
                if noun in player.current_room.items:
                    player.inventory.append(noun)
                    player.current_room.items.remove(noun)
                    print(f"你拿到了 {noun}。")
                else:
                    print("那里没有这个物品。")
                    
            elif verb == "use":
                if noun == "rusty_key" and "sword_sheath" in player.current_room.items:
                    print("钥匙插入剑鞘，咔嗒一声，一柄寒光闪闪的铁剑弹出！")
                    player.inventory.append("iron_sword")
                    player.inventory.remove("rusty_key")
                elif noun == "iron_sword" and player.current_room.name == "Treasure Chamber":
                    print("你挥舞剑砍断锁链，王冠掉落脚边！")
                    player.inventory.append("diamond_crown")
                    player.current_room.items.remove("diamond_crown")
                else:
                    print("无法在此使用该物品。")
                    
            elif verb == "check":
                if noun == "sword_sheath" and noun in player.current_room.items:
                    print("空剑鞘上刻着'王者之剑'的字样。")
                elif noun == "crown" and "diamond_crown" in player.current_room.items:
                    print("王冠闪耀着神秘的蓝光...")
                else:
                    print("看不出有什么特别。")
                    
            elif verb == "inventory":
                print("携带物品:", ', '.join(player.inventory) if player.inventory else "背包空空。")
                
            elif verb == "help":
                print("""
可用命令：
go [方向] - 移动方向
take [物品] - 拾取物品
use [物品] - 使用物品
check [物品] - 检查物品
inventory - 查看背包
quit - 退出游戏
""")
                
            elif verb == "quit":
                print("冒险结束。感谢游玩！")
                break
                
            elif verb == "attack":
                if player.current_room.enemies:
                    enemy = player.current_room.enemies[0]
                    if combat(player, enemy):
                        player.current_room.enemies.remove(enemy)
                else:
                    print("这里没有敌人可以攻击。")
            
            # 胜利条件检测
            if "diamond_crown" in player.inventory and player.current_room.name == "Treasure Chamber":
                print("\n你成功取得王冠！宝库大门自动开启，荣光归于勇者！")
                break
                
            # 失败条件检测
            if player.health <= 0:
                print("\n你倒下了...冒险失败。")
                break
        except Exception as e:
            print(f"游戏过程中发生错误: {e}")

if __name__ == "__main__":
    main()

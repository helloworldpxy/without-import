# Written by HelloWorld05
# Dungeon Quest - 地牢探险游戏
# 玩家将探索一个随机生成的地牢，与怪物战斗，寻找宝藏，最终挑战邪恶的巫妖王。
'''
游戏特点

    完整的地牢探险系统：

        3层随机生成的地牢

        5种不同类型的房间（怪物、宝藏、陷阱、喷泉、商店）

        每层都有独特的Boss

    角色成长系统：

        经验值和等级系统

        击败怪物获得金币和经验

        升级提升属性

    丰富的战斗系统：

        回合制战斗

        攻击、防御属性计算

        使用药水恢复生命

        逃跑机制

    物品和装备系统：

        生命药水

        永久提升属性的药水

        武器和护甲升级

    最终Boss战：

        挑战强大的巫妖王

        拯救王国

如何游玩

    输入你的角色名

    探索地牢房间（使用 'n' 和 's' 移动）

    与怪物战斗，寻找宝藏，避开陷阱

    使用 'u' 使用药水恢复生命

    击败每层的Boss后使用 'd' 进入下一层

    最终目标是击败第三层的巫妖王

游戏指令

    n - 向北移动（上一个房间）

    s - 向南移动（下一个房间）

    d - 向下进入下一层（击败Boss后可用）

    i - 检查角色状态

    u - 使用药水

    h - 显示帮助

    q - 退出游戏

祝你在Dungeon Quest中玩得愉快！
'''


class DungeonQuest:
    def __init__(self):
        self.player = {
            "name": "冒险者",
            "health": 100,
            "max_health": 100,
            "attack": 15,
            "defense": 5,
            "gold": 0,
            "level": 1,
            "exp": 0,
            "potions": 3,
            "weapon": "短剑",
            "armor": "皮甲"
        }
        self.dungeon_level = 1
        self.current_room = 0
        self.game_over = False
        self.victory = False
        self.rooms = []
        self.boss_defeated = False
        self.generate_dungeon()
    
    def generate_dungeon(self):
        # 生成地牢布局 (5个房间)
        self.rooms = []
        room_types = ["empty", "monster", "treasure", "trap", "fountain", "shop"]
        
        # 确保每个地牢层级都有不同的内容
        for i in range(5):
            room_type = room_types[(i + self.dungeon_level) % len(room_types)]
            
            # 最后一个房间总是Boss房间
            if i == 4:
                room_type = "boss" if self.dungeon_level < 3 else "lich_king"
            
            # 创建房间
            room = {"type": room_type, "visited": False}
            
            # 为房间添加特定内容
            if room_type == "monster":
                monsters = ["哥布林", "兽人", "骷髅战士", "巨蜘蛛", "洞穴巨魔"]
                room["monster"] = monsters[(self.dungeon_level + i) % len(monsters)]
                room["health"] = 30 + self.dungeon_level * 10
                room["attack"] = 10 + self.dungeon_level * 3
                room["gold"] = (5 + self.dungeon_level * 3) * (i + 1)
                room["exp"] = 20 + self.dungeon_level * 5
                
            elif room_type == "treasure":
                treasures = ["金箱子", "宝石堆", "古代宝箱", "魔法物品", "王室珠宝"]
                room["treasure"] = treasures[i % len(treasures)]
                room["gold"] = 20 + self.dungeon_level * 10
                room["item"] = "药水" if i % 2 == 0 else "无"
                
            elif room_type == "trap":
                traps = ["毒箭陷阱", "落石陷阱", "地刺陷阱", "火焰陷阱", "魔法陷阱"]
                room["trap"] = traps[i % len(traps)]
                room["damage"] = 15 + self.dungeon_level * 3
                
            elif room_type == "fountain":
                room["effect"] = "heal" if i % 2 == 0 else "blessing"
                
            elif room_type == "shop":
                room["items"] = [
                    {"name": "生命药水", "price": 10, "effect": "heal"},
                    {"name": "攻击药水", "price": 15, "effect": "attack"},
                    {"name": "防御药水", "price": 15, "effect": "defense"},
                    {"name": "钢剑", "price": 30, "effect": "weapon"},
                    {"name": "锁子甲", "price": 40, "effect": "armor"}
                ]
                
            elif room_type == "boss":
                bosses = ["食人魔首领", "双头巨人", "暗影法师"]
                room["boss"] = bosses[self.dungeon_level - 1]
                room["health"] = 100 + self.dungeon_level * 30
                room["attack"] = 20 + self.dungeon_level * 5
                room["gold"] = 50 + self.dungeon_level * 20
                room["exp"] = 100 + self.dungeon_level * 30
                
            elif room_type == "lich_king":
                room["health"] = 300
                room["attack"] = 35
                room["gold"] = 200
                room["exp"] = 500
                
            self.rooms.append(room)
    
    def display_status(self):
        print(f"\n===== 地牢层级: {self.dungeon_level} | 房间: {self.current_room+1}/5 =====")
        print(f"{self.player['name']} - 等级 {self.player['level']} (EXP: {self.player['exp']}/100)")
        print(f"生命: {self.player['health']}/{self.player['max_health']}")
        print(f"武器: {self.player['weapon']}, 护甲: {self.player['armor']}")
        print(f"攻击: {self.player['attack']}, 防御: {self.player['defense']}")
        print(f"金币: {self.player['gold']}, 药水: {self.player['potions']}")
    
    def display_room(self):
        room = self.rooms[self.current_room]
        
        if not room["visited"]:
            if room["type"] == "empty":
                print("\n你进入了一个空房间。这里看起来安全，但也没什么有趣的东西。")
            elif room["type"] == "monster":
                print(f"\n房间里有一只凶恶的{room['monster']}！它朝你冲了过来！")
            elif room["type"] == "treasure":
                print(f"\n你发现了一个{room['treasure']}！里面闪闪发光！")
            elif room["type"] == "trap":
                print(f"\n你触发了{room['trap']}！危险！")
            elif room["type"] == "fountain":
                print("\n你发现了一个神秘的喷泉。水面闪烁着奇异的光芒。")
            elif room["type"] == "shop":
                print("\n你发现了一个地下商店！一个神秘的商人向你招手。")
            elif room["type"] == "boss":
                print(f"\n巨大的{room['boss']}挡住了去路！这是本层的守护者！")
            elif room["type"] == "lich_king":
                print("\n你进入了巫妖王的王座室！冰冷的空气刺痛着你的皮肤。")
                print("巫妖王从冰封王座上站起来：'凡人，你竟敢挑战死亡本身？'")
            room["visited"] = True
        else:
            if room["type"] == "empty":
                print("\n这是一个空房间，你已经探索过了。")
            elif room["type"] == "monster" and room["health"] > 0:
                print(f"\n{room['monster']}仍然在房间里，对你虎视眈眈！")
            else:
                print("\n你回到了之前探索过的房间。")
    
    def handle_room(self):
        room = self.rooms[self.current_room]
        
        if room["type"] == "monster" and room["health"] > 0:
            self.combat(room)
        elif room["type"] == "trap":
            self.trigger_trap(room)
        elif room["type"] == "treasure":
            self.open_treasure(room)
        elif room["type"] == "fountain":
            self.use_fountain(room)
        elif room["type"] == "shop":
            self.visit_shop()
        elif room["type"] == "boss" and room["health"] > 0:
            self.combat(room)
        elif room["type"] == "lich_king":
            self.combat(room)
    
    def combat(self, enemy):
        if "boss" in enemy:
            enemy_name = enemy["boss"]
        elif "monster" in enemy:
            enemy_name = enemy["monster"]
        else:
            enemy_name = "巫妖王"
        
        print(f"\n===== 战斗开始! =====\n")
        
        while self.player["health"] > 0 and enemy["health"] > 0:
            # 玩家攻击
            player_damage = max(1, self.player["attack"] + self.rand(5) - enemy.get("defense", 0))
            enemy["health"] -= player_damage
            print(f"你对{enemy_name}造成了{player_damage}点伤害!")
            
            if enemy["health"] <= 0:
                enemy["health"] = 0
                print(f"\n你击败了{enemy_name}!")
                
                # 获得奖励
                gold = enemy["gold"]
                exp = enemy["exp"]
                self.player["gold"] += gold
                self.player["exp"] += exp
                print(f"获得了 {gold} 金币 和 {exp} 经验值!")
                
                # 检查升级
                if self.player["exp"] >= 100:
                    self.level_up()
                
                # 检查Boss是否被击败
                if enemy["type"] == "boss" or enemy["type"] == "lich_king":
                    if enemy["type"] == "lich_king":
                        self.victory = True
                        self.game_over = True
                        print("\n\n你击败了巫妖王！地牢的诅咒被解除了！")
                        print("恭喜你拯救了王国！你是真正的英雄！")
                    else:
                        self.boss_defeated = True
                        print("\n你击败了本层的守护者！通往下一层的楼梯出现了。")
                return
            
            # 敌人攻击
            enemy_damage = max(1, enemy["attack"] + self.rand(3) - self.player["defense"])
            self.player["health"] -= enemy_damage
            print(f"{enemy_name}对你造成了{enemy_damage}点伤害!")
            print(f"你的生命: {self.player['health']}/{self.player['max_health']}")
            
            if self.player["health"] <= 0:
                self.player["health"] = 0
                print("\n你被击败了...")
                self.game_over = True
                return
            
            # 战斗选项
            print("\n战斗选项:")
            print("1. 继续攻击")
            print("2. 使用药水")
            print("3. 尝试逃跑")
            
            choice = input("选择行动: ")
            if choice == "2":
                if self.player["potions"] > 0:
                    self.player["health"] = min(self.player["max_health"], self.player["health"] + 30)
                    self.player["potions"] -= 1
                    print(f"你喝下了一瓶药水，恢复了30点生命值!")
                    print(f"剩余药水: {self.player['potions']}")
                else:
                    print("你没有药水了!")
            elif choice == "3":
                escape_chance = self.rand(100)
                if escape_chance > 40:
                    print("你成功逃脱了战斗!")
                    return
                else:
                    print("逃跑失败!")
    
    def trigger_trap(self, room):
        damage = room["damage"]
        self.player["health"] -= damage
        print(f"{room['trap']}对你造成了{damage}点伤害!")
        print(f"你的生命: {self.player['health']}/{self.player['max_health']}")
        
        if self.player["health"] <= 0:
            self.player["health"] = 0
            print("\n你被陷阱杀死了...")
            self.game_over = True
    
    def open_treasure(self, room):
        print(f"\n你打开了{room['treasure']}，发现了{room['gold']}金币!")
        self.player["gold"] += room["gold"]
        
        if room["item"] == "药水":
            self.player["potions"] += 1
            print("你还发现了一瓶生命药水!")
        
        # 标记为已获取
        room["gold"] = 0
        room["item"] = "无"
    
    def use_fountain(self, room):
        if room["effect"] == "heal":
            heal_amount = 40
            self.player["health"] = min(self.player["max_health"], self.player["health"] + heal_amount)
            print(f"你喝了喷泉的水，恢复了{heal_amount}点生命值!")
        else:
            self.player["attack"] += 2
            self.player["defense"] += 2
            print("喷泉的祝福使你变得更加强大!")
            print(f"攻击力+2, 防御力+2")
    
    def visit_shop(self):
        print("\n商人: '欢迎，旅行者！看看我的商品吧:'")
        print("==================================")
        for i, item in enumerate(self.rooms[self.current_room]["items"], 1):
            print(f"{i}. {item['name']} - {item['price']}金币")
        print("==================================")
        print(f"你有 {self.player['gold']} 金币")
        
        choice = input("购买物品编号 (或输入0离开): ")
        if choice == "0":
            return
        
        try:
            choice = int(choice)
            if 1 <= choice <= len(self.rooms[self.current_room]["items"]):
                item = self.rooms[self.current_room]["items"][choice-1]
                
                if self.player["gold"] >= item["price"]:
                    self.player["gold"] -= item["price"]
                    
                    if item["effect"] == "heal":
                        self.player["potions"] += 1
                        print(f"购买了 {item['name']}!")
                    elif item["effect"] == "attack":
                        self.player["attack"] += 5
                        print(f"攻击力永久增加5点!")
                    elif item["effect"] == "defense":
                        self.player["defense"] += 5
                        print(f"防御力永久增加5点!")
                    elif item["effect"] == "weapon":
                        self.player["weapon"] = "钢剑"
                        self.player["attack"] += 8
                        print(f"装备了钢剑! 攻击力+8")
                    elif item["effect"] == "armor":
                        self.player["armor"] = "锁子甲"
                        self.player["defense"] += 10
                        print(f"装备了锁子甲! 防御力+10")
                    
                    # 移除已购买的商品
                    self.rooms[self.current_room]["items"].pop(choice-1)
                else:
                    print("金币不足!")
            else:
                print("无效的选择")
        except ValueError:
            print("无效的输入")
    
    def level_up(self):
        self.player["level"] += 1
        self.player["exp"] = self.player["exp"] - 100
        
        # 提升属性
        self.player["max_health"] += 20
        self.player["health"] = self.player["max_health"]
        self.player["attack"] += 5
        self.player["defense"] += 3
        
        print("\n\n*** 升级了! ***")
        print(f"恭喜你达到等级 {self.player['level']}!")
        print(f"最大生命值增加20, 攻击力增加5, 防御力增加3")
    
    def move(self, direction):
        if direction == "n" and self.current_room > 0:
            self.current_room -= 1
        elif direction == "s" and self.current_room < 4:
            self.current_room += 1
        elif direction == "d" and self.boss_defeated:
            if self.dungeon_level < 3:
                self.dungeon_level += 1
                self.current_room = 0
                self.boss_defeated = False
                self.generate_dungeon()
                print(f"\n你进入了地牢的第{self.dungeon_level}层...")
            else:
                print("\n你已经在最底层了")
        else:
            print("\n无法朝那个方向移动")
    
    def rand(self, n):
        # 简单的伪随机数生成器
        seed = (id(self) + self.current_room * 100 + self.dungeon_level * 10) % 1000
        return (seed * 73129 + 95121) % n + 1
    
    def show_help(self):
        print("\n===== 游戏指令 =====")
        print("n - 向北移动 (上一个房间)")
        print("s - 向南移动 (下一个房间)")
        print("d - 向下进入下一层 (击败Boss后可用)")
        print("i - 检查状态")
        print("u - 使用药水")
        print("h - 显示帮助")
        print("q - 退出游戏")
        print("=====================")
    
    def use_potion(self):
        if self.player["potions"] > 0:
            self.player["health"] = min(self.player["max_health"], self.player["health"] + 30)
            self.player["potions"] -= 1
            print(f"你喝下了一瓶药水，恢复了30点生命值!")
            print(f"剩余药水: {self.player['potions']}")
        else:
            print("你没有药水了!")
    
    def play(self):
        print("欢迎来到 Dungeon Quest!")
        print("=======================")
        print("你是一位勇敢的冒险者，探索被诅咒的地牢。")
        print("击败巫妖王，拯救王国!")
        print("输入 'h' 查看游戏指令")
        
        self.player["name"] = input("\n请输入你的名字: ")
        
        while not self.game_over and not self.victory:
            self.display_status()
            self.display_room()
            self.handle_room()
            
            if self.game_over or self.victory:
                break
            
            print("\n可行动作: ")
            print("n - 向北移动 (上一个房间)")
            print("s - 向南移动 (下一个房间)")
            if self.boss_defeated:
                print("d - 向下进入下一层")
            print("i - 检查状态")
            print("u - 使用药水")
            print("h - 显示帮助")
            print("q - 退出游戏")
            
            action = input("\n选择行动: ").lower()
            
            if action == "n" or action == "s" or (action == "d" and self.boss_defeated):
                self.move(action)
            elif action == "i":
                self.display_status()
            elif action == "u":
                self.use_potion()
            elif action == "h":
                self.show_help()
            elif action == "q":
                print("\n感谢游玩 Dungeon Quest!")
                self.game_over = True
            else:
                print("无效指令! 输入 'h' 查看帮助")
        
        if self.victory:
            print("\n\n====== 游戏胜利! ======")
            print(f"恭喜 {self.player['name']}，你成功击败了巫妖王！")
            print("王国因你的英勇行为而获救！")
            print("=======================")
        elif self.game_over:
            print("\n\n====== 游戏结束 ======")
            print(f"很遗憾，{self.player['name']}的冒险结束了...")
            print("=====================")

# 启动游戏
if __name__ == "__main__":
    game = DungeonQuest()
    game.play()
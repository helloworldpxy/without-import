# 文字枪战游戏

# 游戏状态
class GameState:
    def __init__(self):
        self.player = None
        self.location = "安全区"
        self.day = 1
        self.game_over = False
        self.mission_completed = False
        
    def advance_day(self):
        self.day += 1
        if self.day > 7:
            self.game_over = True
            
    def display_status(self):
        print(f"\n=== 第 {self.day} 天 ===")
        print(f"位置: {self.location}")
        self.player.display_status()

# 角色类
class Character:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.max_health = 100
        self.weapon = None
        self.armor = None
        self.inventory = []
        self.money = 100
        self.kills = 0
        self.level = 1
        self.exp = 0
        self.exp_to_next_level = 100
        
    def display_status(self):
        print(f"\n{self.name} 状态:")
        print(f"生命值: {self.health}/{self.max_health}")
        print(f"武器: {self.weapon.name if self.weapon else '无'}")
        print(f"护甲: {self.armor.name if self.armor else '无'}")
        print(f"金钱: ${self.money}")
        print(f"击杀数: {self.kills}")
        print(f"等级: {self.level} (经验: {self.exp}/{self.exp_to_next_level})")
        
    def take_damage(self, damage):
        if self.armor:
            damage = max(1, damage - self.armor.defense)
        self.health -= damage
        if self.health < 0:
            self.health = 0
        return damage
        
    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)
        
    def add_exp(self, amount):
        self.exp += amount
        if self.exp >= self.exp_to_next_level:
            self.level_up()
            
    def level_up(self):
        self.level += 1
        self.exp -= self.exp_to_next_level
        self.exp_to_next_level = int(self.exp_to_next_level * 1.5)
        self.max_health += 20
        self.health = self.max_health
        print(f"\n恭喜！{self.name} 升级到 {self.level} 级！")
        print(f"最大生命值增加到 {self.max_health}")

# 物品基类
class Item:
    def __init__(self, name, value):
        self.name = name
        self.value = value

# 武器类
class Weapon(Item):
    def __init__(self, name, damage, value, ammo_capacity=0):
        super().__init__(name, value)
        self.damage = damage
        self.ammo_capacity = ammo_capacity
        self.ammo = ammo_capacity
        
    def attack(self):
        if self.ammo_capacity > 0:
            if self.ammo <= 0:
                print(f"{self.name} 没有弹药了！")
                return 0
            self.ammo -= 1
        return self.damage

# 护甲类
class Armor(Item):
    def __init__(self, name, defense, value):
        super().__init__(name, value)
        self.defense = defense

# 消耗品类
class Consumable(Item):
    def __init__(self, name, heal_amount, value):
        super().__init__(name, value)
        self.heal_amount = heal_amount

# 敌人类
class Enemy:
    def __init__(self, name, health, weapon, difficulty):
        self.name = name
        self.health = health
        self.max_health = health
        self.weapon = weapon
        self.difficulty = difficulty
        
    def display_status(self):
        print(f"\n{self.name} (难度: {self.difficulty})")
        print(f"生命值: {self.health}/{self.max_health}")
        print(f"武器: {self.weapon.name}")
        
    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
        return damage
        
    def attack(self):
        return self.weapon.attack()

# 商店类
class Shop:
    def __init__(self):
        self.inventory = [
            Weapon("手枪", 25, 50, 6),
            Weapon("霰弹枪", 40, 100, 2),
            Weapon("冲锋枪", 20, 150, 30),
            Weapon("狙击步枪", 60, 300, 5),
            Armor("防弹背心", 10, 80),
            Armor("战术护甲", 20, 200),
            Consumable("急救包", 30, 30),
            Consumable("医疗箱", 70, 70)
        ]
        
    def display_inventory(self):
        print("\n=== 商店库存 ===")
        for i, item in enumerate(self.inventory):
            if isinstance(item, Weapon):
                print(f"{i+1}. {item.name} - 伤害: {item.damage} 弹药: {item.ammo_capacity} - ${item.value}")
            elif isinstance(item, Armor):
                print(f"{i+1}. {item.name} - 防御: {item.defense} - ${item.value}")
            elif isinstance(item, Consumable):
                print(f"{i+1}. {item.name} - 治疗: {item.heal_amount} - ${item.value}")

# 游戏逻辑
class TextShooterGame:
    def __init__(self):
        self.state = GameState()
        self.shop = Shop()
        self.enemies = [
            Enemy("街头混混", 60, Weapon("小刀", 10, 0), "简单"),
            Enemy("黑帮成员", 80, Weapon("手枪", 25, 0), "中等"),
            Enemy("职业杀手", 120, Weapon("冲锋枪", 20, 0), "困难"),
            Enemy("黑帮头目", 200, Weapon("霰弹枪", 40, 0), "极难")
        ]
        self.missions = [
            "清除街头混混",
            "消灭黑帮成员",
            "刺杀职业杀手",
            "击败黑帮头目"
        ]
        self.current_mission = 0
        self.game_over = False
        
    def start_game(self):
        print("=== 文字枪战游戏 ===")
        print("在一个犯罪横行的城市里，你是一名雇佣兵，任务是清理城市的黑帮势力。")
        print("你有7天时间完成所有任务，否则城市将陷入混乱...")
        
        player_name = self.get_input("请输入你的名字: ")
        self.state.player = Character(player_name)
        self.state.player.inventory.append(Weapon("小刀", 10, 0))
        
        print(f"\n欢迎, {player_name}! 你从一把小刀开始你的任务。")
        
        while not self.state.game_over and not self.game_over:
            self.state.display_status()
            self.main_menu()
            
        if self.state.game_over:
            print("\n=== 游戏结束 ===")
            print("7天过去了，你未能完成所有任务...")
            print("城市陷入了黑帮的混乱统治中。")
        elif self.game_over:
            if self.state.player.health <= 0:
                print("\n=== 游戏结束 ===")
                print("你在战斗中阵亡...")
            elif self.mission_completed:
                print("\n=== 任务完成 ===")
                print("恭喜你！你成功清除了城市中的所有黑帮势力！")
                print(f"最终等级: {self.state.player.level}")
                print(f"总击杀数: {self.state.player.kills}")
                print(f"剩余金钱: ${self.state.player.money}")
        
    def get_input(self, prompt, options=None):
        while True:
            user_input = input(prompt).strip()
            if not options:
                return user_input
                
            if user_input in options:
                return user_input
                
            print("无效选择，请重试。")
    
    def main_menu(self):
        print("\n=== 主菜单 ===")
        print("1. 探索城市")
        print("2. 访问商店")
        print("3. 查看背包")
        print("4. 休息一天")
        print("5. 查看任务")
        print("6. 退出游戏")
        
        choice = self.get_input("请选择: ", ["1", "2", "3", "4", "5", "6"])
        
        if choice == "1":
            self.explore()
        elif choice == "2":
            self.visit_shop()
        elif choice == "3":
            self.view_inventory()
        elif choice == "4":
            self.rest()
        elif choice == "5":
            self.view_missions()
        elif choice == "6":
            self.game_over = True
    
    def explore(self):
        self.state.location = "危险区"
        print("\n你进入了城市的危险区域...")
        
        # 遇到敌人的概率
        enemy_chance = 70  # 70% 遇到敌人
        
        # 生成随机数
        rand_val = hash(str(hash(str(self.state.day) + str(self.state.player.health)))) % 100
        
        if rand_val < enemy_chance:
            # 根据当前任务进度选择敌人
            enemy_index = min(self.current_mission, len(self.enemies)-1)
            enemy = self.enemies[enemy_index]
            print(f"\n你遇到了一个 {enemy.name}!")
            self.combat(enemy)
        else:
            # 找到物品
            items = [
                ("急救包", Consumable("急救包", 30, 30)),
                ("手枪弹药", "ammo"),
                ("$50", "money")
            ]
            found_item = items[hash(str(self.state.day)) % len(items)]
            
            if found_item[1] == "money":
                amount = 50
                self.state.player.money += amount
                print(f"\n你发现了 ${amount}!")
            elif found_item[1] == "ammo":
                if self.state.player.weapon and self.state.player.weapon.ammo_capacity > 0:
                    self.state.player.weapon.ammo = min(
                        self.state.player.weapon.ammo_capacity, 
                        self.state.player.weapon.ammo + 6
                    )
                    print(f"\n你发现了一些弹药！{self.state.player.weapon.name} 弹药增加了。")
                else:
                    print("\n你发现了一些弹药，但没有可用的武器。")
            else:
                item = found_item[1]
                self.state.player.inventory.append(item)
                print(f"\n你发现了一个 {found_item[0]}!")
    
    def visit_shop(self):
        self.state.location = "商店"
        print("\n欢迎来到武器商店！")
        
        while True:
            self.shop.display_inventory()
            print(f"\n你的金钱: ${self.state.player.money}")
            print("b. 返回")
            
            choice = self.get_input("请选择要购买的物品编号 (或输入 'b' 返回): ")
            
            if choice.lower() == "b":
                break
                
            try:
                index = int(choice) - 1
                if 0 <= index < len(self.shop.inventory):
                    item = self.shop.inventory[index]
                    if self.state.player.money >= item.value:
                        self.state.player.money -= item.value
                        
                        if isinstance(item, Weapon) or isinstance(item, Armor) or isinstance(item, Consumable):
                            # 创建新实例，避免引用问题
                            if isinstance(item, Weapon):
                                new_item = Weapon(item.name, item.damage, item.value, item.ammo_capacity)
                            elif isinstance(item, Armor):
                                new_item = Armor(item.name, item.defense, item.value)
                            else:
                                new_item = Consumable(item.name, item.heal_amount, item.value)
                            
                            self.state.player.inventory.append(new_item)
                            print(f"\n你购买了 {item.name}!")
                        else:
                            print("\n购买失败: 物品类型无效")
                    else:
                        print("\n金钱不足！")
                else:
                    print("\n无效选择！")
            except ValueError:
                print("\n请输入有效的数字！")
    
    def view_inventory(self):
        print("\n=== 你的背包 ===")
        
        if not self.state.player.inventory:
            print("背包是空的！")
            return
            
        for i, item in enumerate(self.state.player.inventory):
            print(f"{i+1}. {item.name}")
            
        print("\ne. 装备武器")
        print("u. 使用物品")
        print("d. 丢弃物品")
        print("b. 返回")
        
        choice = self.get_input("请选择: ", [str(i+1) for i in range(len(self.state.player.inventory))] + ["e", "u", "d", "b"])
        
        if choice == "b":
            return
        elif choice == "e":
            self.equip_weapon()
        elif choice == "u":
            self.use_item()
        elif choice == "d":
            self.discard_item()
        else:
            index = int(choice) - 1
            item = self.state.player.inventory[index]
            print(f"\n{item.name} 详情:")
            if isinstance(item, Weapon):
                print(f"类型: 武器")
                print(f"伤害: {item.damage}")
                print(f"弹药: {item.ammo}/{item.ammo_capacity}" if item.ammo_capacity > 0 else "无限弹药")
            elif isinstance(item, Armor):
                print(f"类型: 护甲")
                print(f"防御: {item.defense}")
            elif isinstance(item, Consumable):
                print(f"类型: 消耗品")
                print(f"治疗量: {item.heal_amount}")
    
    def equip_weapon(self):
        weapons = [item for item in self.state.player.inventory if isinstance(item, Weapon)]
        
        if not weapons:
            print("\n你没有武器可装备！")
            return
            
        print("\n选择要装备的武器:")
        for i, weapon in enumerate(weapons):
            print(f"{i+1}. {weapon.name} - 伤害: {weapon.damage}")
            
        choice = self.get_input("请选择: ", [str(i+1) for i in range(len(weapons))])
        index = int(choice) - 1
        
        self.state.player.weapon = weapons[index]
        print(f"\n你装备了 {weapons[index].name}!")
    
    def use_item(self):
        consumables = [item for item in self.state.player.inventory if isinstance(item, Consumable)]
        
        if not consumables:
            print("\n你没有消耗品可用！")
            return
            
        print("\n选择要使用的物品:")
        for i, item in enumerate(consumables):
            print(f"{i+1}. {item.name} - 治疗: {item.heal_amount}")
            
        choice = self.get_input("请选择: ", [str(i+1) for i in range(len(consumables))])
        index = int(choice) - 1
        
        item = consumables[index]
        self.state.player.heal(item.heal_amount)
        self.state.player.inventory.remove(item)
        print(f"\n你使用了 {item.name}, 恢复了 {item.heal_amount} 点生命值!")
    
    def discard_item(self):
        if not self.state.player.inventory:
            print("\n背包是空的！")
            return
            
        print("\n选择要丢弃的物品:")
        for i, item in enumerate(self.state.player.inventory):
            print(f"{i+1}. {item.name}")
            
        choice = self.get_input("请选择: ", [str(i+1) for i in range(len(self.state.player.inventory))])
        index = int(choice) - 1
        
        item = self.state.player.inventory[index]
        self.state.player.inventory.remove(item)
        print(f"\n你丢弃了 {item.name}!")
    
    def rest(self):
        heal_amount = 30
        self.state.player.heal(heal_amount)
        print(f"\n你休息了一天，恢复了 {heal_amount} 点生命值。")
        self.state.advance_day()
    
    def view_missions(self):
        print("\n=== 当前任务 ===")
        for i, mission in enumerate(self.missions):
            status = "✓" if i < self.current_mission else " " if i == self.current_mission else " "
            print(f"{i+1}. [{status}] {mission}")
        
        print("\n你有7天时间完成所有任务。")
        print(f"当前是第 {self.state.day} 天。")
    
    def combat(self, enemy):
        print(f"\n=== 战斗开始! ===")
        print(f"你 vs {enemy.name}")
        
        # 确保玩家有武器
        if not self.state.player.weapon:
            weapons = [item for item in self.state.player.inventory if isinstance(item, Weapon)]
            if weapons:
                self.state.player.weapon = weapons[0]
                print(f"你匆忙装备了 {self.state.player.weapon.name}!")
            else:
                print("你没有武器！只能用拳头战斗...")
                self.state.player.weapon = Weapon("拳头", 5, 0)
        
        while self.state.player.health > 0 and enemy.health > 0:
            print("\n=== 战斗回合 ===")
            self.state.player.display_status()
            enemy.display_status()
            
            # 玩家行动
            print("\n行动:")
            print("1. 攻击")
            print("2. 使用物品")
            print("3. 逃跑 (50% 成功率)")
            
            action = self.get_input("请选择: ", ["1", "2", "3"])
            
            if action == "1":  # 攻击
                damage = self.state.player.weapon.attack()
                if damage > 0:
                    actual_damage = enemy.take_damage(damage)
                    print(f"\n你用 {self.state.player.weapon.name} 攻击了 {enemy.name}, 造成了 {actual_damage} 点伤害!")
                else:
                    print("\n攻击失败!")
            elif action == "2":  # 使用物品
                self.use_item_in_combat()
                continue  # 使用物品后不进入敌人回合
            elif action == "3":  # 逃跑
                # 逃跑成功率50%
                rand_val = hash(str(hash(str(self.state.player.health) + str(enemy.health)))) % 100
                if rand_val < 50:
                    print("\n你成功逃脱了战斗!")
                    self.state.location = "安全区"
                    return
                else:
                    print("\n逃跑失败!")
            
            # 敌人行动
            if enemy.health > 0:
                damage = enemy.attack()
                actual_damage = self.state.player.take_damage(damage)
                print(f"\n{enemy.name} 用 {enemy.weapon.name} 攻击了你, 造成了 {actual_damage} 点伤害!")
                
                if self.state.player.health <= 0:
                    print("\n你被击败了...")
                    self.game_over = True
                    return
        
        # 战斗结束
        if enemy.health <= 0:
            print(f"\n你击败了 {enemy.name}!")
            reward = enemy.difficulty * 50
            exp = enemy.difficulty * 30
            
            self.state.player.money += reward
            self.state.player.add_exp(exp)
            self.state.player.kills += 1
            
            print(f"获得 ${reward} 和 {exp} 经验值!")
            
            # 检查任务完成情况
            if self.current_mission < len(self.missions):
                self.current_mission += 1
                if self.current_mission >= len(self.missions):
                    self.mission_completed = True
                    self.game_over = True
                    print("\n恭喜！你完成了所有任务！")
        
        self.state.location = "安全区"
    
    def use_item_in_combat(self):
        consumables = [item for item in self.state.player.inventory if isinstance(item, Consumable)]
        
        if not consumables:
            print("\n你没有消耗品可用！")
            return
            
        print("\n选择要使用的物品:")
        for i, item in enumerate(consumables):
            print(f"{i+1}. {item.name} - 治疗: {item.heal_amount}")
            
        choice = self.get_input("请选择: ", [str(i+1) for i in range(len(consumables))])
        index = int(choice) - 1
        
        item = consumables[index]
        self.state.player.heal(item.heal_amount)
        self.state.player.inventory.remove(item)
        print(f"\n你使用了 {item.name}, 恢复了 {item.heal_amount} 点生命值!")

# 启动游戏
if __name__ == "__main__":
    game = TextShooterGame()
    game.start_game()
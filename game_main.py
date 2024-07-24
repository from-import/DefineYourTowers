import pyglet
from pyglet import shapes
from Bullet import Bullet
import math

# 创建一个窗口，设置窗口的宽度、高度和标题
window = pyglet.window.Window(width=1000, height=600, caption="Pyglet Demo")

# 加载图像资源，用于个体显示
image = pyglet.resource.image('assets/Round/bear.png')

# 定义一个实体类，表示游戏中的个体
class Entity:
    def __init__(self, name, health, attack, defense, x, y, attack_frequency, direction, faction):
        # 初始化个体的属性
        self.name = name  # 个体的名称
        self.max_health = health  # 最大生命值
        self.health = health  # 当前生命值
        self.attack = attack  # 攻击力
        self.defense = defense  # 防御力
        self.x = x  # 个体的x坐标
        self.y = y  # 个体的y坐标
        self.width = image.width  # 图像的宽度
        self.height = image.height  # 图像的高度
        self.bullets = []  # 子弹列表
        self.attack_frequency = attack_frequency  # 攻击频率（秒）
        self.direction = direction  # 朝向（度）
        self.faction = faction  # 阵营

    # 个体受到伤害的方法
    def take_damage(self, damage):
        damage_taken = max(damage - self.defense, 0)  # 计算实际受到的伤害
        self.health -= damage_taken  # 减少生命值
        print(f"{self.name} took {damage_taken} damage and has {self.health} health left.")
        if self.health <= 0:  # 如果生命值小于等于0，表示个体被击败
            print(f"{self.name} has been defeated。")
            return False  # 返回False表示个体被击败
        return True  # 返回True表示个体仍然存活

    # 发射子弹的方法
    def fire_bullet(self):
        bullet = Bullet(self.x + self.width // 2, self.y + self.height // 2, 500, self.attack, self.direction, window, self.faction)
        # 创建子弹对象，并将其添加到子弹列表中
        self.bullets.append(bullet)

    # 自定义超级攻击的方法
    def superAttack(self, custom_attack, direction, speed, damage):
        bullet = Bullet(self.x + self.width // 2, self.y + self.height // 2, speed, damage, direction, window, self.faction)
        # 创建自定义子弹对象，并将其添加到子弹列表中
        self.bullets.append(bullet)

    # 更新子弹的方法
    def update_bullets(self, dt):
        for bullet in self.bullets:
            bullet.update(dt)  # 更新子弹的位置
            # 检查子弹是否碰撞到任何实体
            for entity in entities:
                if entity != self and bullet.collides_with(entity):  # 忽略自己
                    if entity.faction != bullet.faction:  # 如果不是同阵营
                        if not entity.take_damage(bullet.damage):  # 如果目标被击败
                            entities.remove(entity)  # 从实体列表中移除目标
                        bullet.active = False  # 设置子弹为不活跃
        self.bullets = [bullet for bullet in self.bullets if bullet.active]  # 只保留活跃的子弹

    # 绘制个体的方法
    def draw(self):
        image.blit(self.x, self.y)  # 绘制个体的图像
        self.draw_health_bar()  # 绘制生命值条
        for bullet in self.bullets:  # 绘制所有子弹
            bullet.draw()

    # 绘制生命值条的方法
    def draw_health_bar(self):
        health_percentage = self.health / self.max_health  # 计算生命值百分比
        bar_length = self.width  # 血条的长度
        bar_height = 10  # 血条的高度

        if health_percentage > 0.5:
            color = (0, 255, 0)  # 绿色
        else:
            color = (255, 0, 0)  # 红色

        # 创建背景血条和前景血条
        background_bar = shapes.Rectangle(self.x, self.y + self.height + 5, bar_length, bar_height, color=(50, 50, 50))
        health_bar = shapes.Rectangle(self.x, self.y + self.height + 5, bar_length * health_percentage, bar_height, color=color)

        # 绘制血条
        background_bar.draw()
        health_bar.draw()

    # 开始攻击的方法，不需要指定目标
    def start_attacking(self):
        pyglet.clock.schedule_interval(self.perform_attack, self.attack_frequency)  # 按攻击频率调度攻击事件

    # 执行攻击的方法
    def perform_attack(self, dt):
        self.fire_bullet()  # 直接发射子弹


# 创建个体列表
entities = []

# 创建三个个体
entity1 = Entity("Knight1", 100, 20, 10, 0, 400, 2, 0, "A")  # 攻击频率为2秒，朝向为0度（向右）
entity2 = Entity("Knight2", 80, 15, 5, 800, 400, 1.5, 180, "B")  # 攻击频率为1.5秒，朝向为180度（向左）
entity3 = Entity("Knight3", 100, 30, 10, 0, 100, 0.5, 20, "A")  # 攻击频率为0.5秒，朝向为45度（向右）

# 将个体添加到个体列表中
entities.append(entity1)
entities.append(entity2)
entities.append(entity3)

# 显示个体信息
print(f"{entity1.name}: Health={entity1.health}, Attack={entity1.attack}, Defense={entity1.defense}")
print(f"{entity2.name}: Health={entity2.health}, Attack={entity2.attack}, Defense={entity2.defense}")
print(f"{entity3.name}: Health={entity3.health}, Attack={entity3.attack}, Defense={entity3.defense}")

# 开始个体间的攻击
entity1.start_attacking()
entity2.start_attacking()
entity3.start_attacking()

# 执行自定义超级攻击
entity1.superAttack(custom_attack="Super Attack", direction=45, speed=700, damage=50)
entity2.superAttack(custom_attack="Super Attack", direction=90, speed=700, damage=50)
entity3.superAttack(custom_attack="Super Attack", direction=135, speed=700, damage=50)

# 处理绘制事件
@window.event
def on_draw():
    window.clear()  # 清除窗口
    for entity in entities:  # 绘制所有个体
        entity.draw()

# 更新方法，包含垃圾回收机制
def update(dt):
    # 更新所有个体的子弹
    for entity in entities:
        entity.update_bullets(dt)

    # 垃圾回收：删除被击败的个体
    for entity in entities[:]:
        if entity.health <= 0:
            entities.remove(entity)

    # 垃圾回收：删除不活跃的子弹
    for entity in entities:
        entity.bullets = [bullet for bullet in entity.bullets if bullet.active]

# 设置定时器，每秒更新60次
pyglet.clock.schedule_interval(update, 1 / 60.0)

# 运行Pyglet事件循环
pyglet.app.run()
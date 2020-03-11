class Settings():
    #存储外星人入侵的所有设置大的类
    def __init__(self):
        """初始化游戏的设置"""
        #屏幕设置
        self.screen_width=1200
        self.screen_height=800
        self.bg_color=(190,237,199)
        
        #飞船设置
        self.ship_limit=3
        
        #子弹设置
        self.bullet_width=1100
        self.bullet_height=15
        self.bullet_color=60,60,60
        
        #alien设置
        self.fleet_drop_speed=10
        self.fleet_direction=1
        #加快游戏节奏
        self.speedup_scale=1.1
        self.score_scale=100
        self.initializee_dynamic_settings()
    def initializee_dynamic_settings(self):
        """初始化随游戏变化的设置"""
        self.ship_speed_factor=1.5
        self.bullet_speed_factor=10
        self.alien_speed_factor=1
        #1向右，-1向左
        self.fleet_dirction=1
        #计分
        self.alien_points=150
    def increase_speed(self):
        """提高速度设置"""
        self.ship_speed_factor*=self.speedup_scale
        self.bullet_speed_factor*=self.speedup_scale
        self.alien_speed_factor*=self.speedup_scale
        self.alien_points=int(self.alien_points*self.score_scale)
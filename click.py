import tkinter as tk
import random

class UltimateClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("絵文字クリッカーゲーム Extreme")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        #ゲーム変数
        self.score = 0
        self.coin_level = 1
        self.range_level = 1
        self.dvd_level = 0      # 初期は未解放(0) 最大10枚
        self.basket_level = 0   # 初期は未解放(0) 最大5

        #背景
        self.canvas = tk.Canvas(root, width=800, height=600, bg="white", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        #データ管理用リスト
        self.coins = []
        self.dvds = []
        self.basket = None
        self.star = None  # 流れ星のデータ

        #UIの作成
        self.score_text = self.canvas.create_text(200, 35, text=f"ポイント: {self.score} pt", fill="orange", font=("MS Gothic", 26, "bold"), anchor="w")
        
        #アップグレードメニュー用のグループ
        self.menu_open = False
        self.menu_items = []

        #左上のメニュー開閉ボタン
        self.menu_btn_rect = self.canvas.create_rectangle(15, 15, 180, 55, fill="orange", outline="")
        self.menu_btn_text = self.canvas.create_text(25, 35, text="🛠 アップグレード", fill="white", font=("MS Gothic", 14, "bold"), anchor="w")

        #マウスクリック範囲を示すインジケーター
        self.click_range_circle = self.canvas.create_oval(
            -100, -100, -100, -100, 
            outline="orange", width=1, dash=(4, 4)
        )

        #イベントのバインド
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<Button-1>", self.on_click)
        
        #デバッグ用：F1キーで500万ポイント獲得
        self.root.bind("<F1>", self.add_debug_score)

        #最初のコインを降らせる
        for _ in range(5):
            self.spawn_coin()
            
        #ゲームループ開始
        self.game_loop()

    #コスト計算
    def get_coin_cost(self): return 1000 * (2 ** (self.coin_level - 1))
    def get_range_cost(self): return 2000 * (2 ** (self.range_level - 1))
    def get_dvd_cost(self): return 5000 * (2 ** self.dvd_level)
    def get_basket_cost(self): return 4000 * (2 ** self.basket_level)

    #プレイヤーの現在のクリック判定半径を取得する関数
    def get_click_radius(self):
        return 20 + (self.range_level * 12) # 拡大の恩恵を感じやすくするためさらに少し広げました

    def spawn_coin(self):
        x = random.randint(50, 750)
        y = random.randint(-80, -40)
        speed = random.randint(2, 5)
        
        # コイン自体のグラフィックサイズ（半径換算で約20ピクセル）
        radius = 20
        
        coin_id = self.canvas.create_text(x, y, text="🪙", font=("Segoe UI Emoji", 30), fill="#FFD700")
        self.coins.append({"id": coin_id, "x": x, "y": y, "speed": speed, "radius": radius})

    def spawn_dvd(self):
        vx = random.choice([-5, -4, 4, 5])
        vy = random.choice([-4, -3, 3, 4])
        dvd_id = self.canvas.create_text(400, 300, text="💿", font=("Segoe UI Emoji", 30))
        self.dvds.append({"id": dvd_id, "x": 400, "y": 300, "vx": vx, "vy": vy})

    def spawn_shooting_star(self):
        if self.star is not None: return
        
        x = random.randint(400, 800)
        y = -50
        vx = -8
        vy = 6
        radius = 25 # 流れ星のサイズ
        
        star_id = self.canvas.create_text(x, y, text="☄️", font=("Segoe UI Emoji", 35))
        self.star = {"id": star_id, "x": x, "y": y, "vx": vx, "vy": vy, "radius": radius}

    def draw_menu(self):
        if not self.menu_open: return
        
        bg = self.canvas.create_rectangle(15, 65, 500, 340, fill="#fff3e0", outline="orange", width=2)
        self.menu_items.append(bg)

        upgrades = [
            (f"① コイン量UP (Lv.{self.coin_level}) コスト:{self.get_coin_cost()}pt", "#ffb74d"),
            (f"② 範囲拡大 (Lv.{self.range_level}/5) " + ("MAX" if self.range_level >= 5 else f"コスト:{self.get_range_cost()}pt"), "#ffb74d"),
            (f"③ 反射DVD枚数 (Lv.{self.dvd_level}/10) " + ("MAX" if self.dvd_level >= 10 else f"コスト:{self.get_dvd_cost()}pt"), "#ffb74d"),
            (f"④ 自動回収かご (Lv.{self.basket_level}/5) " + ("MAX" if self.basket_level >= 5 else f"コスト:{self.get_basket_cost()}pt"), "#ffb74d")
        ]

        for i, (txt, color) in enumerate(upgrades):
            y1 = 80 + (i * 60)
            rect = self.canvas.create_rectangle(30, y1, 485, y1 + 45, fill=color, outline="")
            t = self.canvas.create_text(40, y1 + 22, text=txt, fill="white", font=("MS Gothic", 12, "bold"), anchor="w")
            self.menu_items.extend([rect, t])

    def clear_menu(self):
        for item in self.menu_items:
            self.canvas.delete(item)
        self.menu_items.clear()

    def add_debug_score(self, event):
        self.score += 5000000
        self.canvas.itemconfig(self.score_text, text=f"ポイント: {self.score} pt")
        if self.menu_open:
            self.clear_menu()
            self.draw_menu()

    def on_mouse_move(self, event):
        mx, my = event.x, event.y

        #マウスに追従するオレンジ点線サークルの大きさを更新
        p_radius = self.get_click_radius()
        self.canvas.coords(self.click_range_circle, mx - p_radius, my - p_radius, mx + p_radius, my + p_radius)

        #かごの移動処理
        if self.basket_level > 0:
            max_width = 800 // 3
            width = 60 + (self.basket_level * 40)
            if width > max_width: width = max_width
            
            y = 550
            x1 = mx - width // 2
            x2 = mx + width // 2

            if self.basket is None:
                self.basket = {
                    "id": self.canvas.create_text(mx, y, text="🧺", font=("Segoe UI Emoji", 24)),
                    "width": width, "x1": x1, "x2": x2, "y": y
                }
            else:
                self.basket["width"] = width
                self.basket["x1"] = x1
                self.basket["x2"] = x2
                self.canvas.itemconfig(self.basket["id"], font=("Segoe UI Emoji", 20 + self.basket_level * 4))
                self.canvas.coords(self.basket["id"], mx, y)

    def on_click(self, event):
        mx, my = event.x, event.y

        #メニューボタンのクリック判定
        if 15 <= mx <= 180 and 15 <= my <= 55:
            self.menu_open = not self.menu_open
            if self.menu_open: self.draw_menu()
            else: self.clear_menu()
            return

        #メニューが開いている時のショップボタン判定
        if self.menu_open:
            if 30 <= mx <= 485:
                # ① コイン量
                if 80 <= my <= 125:
                    cost = self.get_coin_cost()
                    if self.score >= cost:
                        self.score -= cost
                        self.coin_level += 1
                # ② 範囲拡大
                elif 140 <= my <= 185 and self.range_level < 5:
                    cost = self.get_range_cost()
                    if self.score >= cost:
                        self.score -= cost
                        self.range_level += 1
                        p_radius = self.get_click_radius()
                        self.canvas.coords(self.click_range_circle, mx - p_radius, my - p_radius, mx + p_radius, my + p_radius)
                # ③ DVD枚数アップ
                elif 200 <= my <= 245 and self.dvd_level < 10:
                    cost = self.get_dvd_cost()
                    if self.score >= cost:
                        self.score -= cost
                        self.dvd_level += 1
                        self.spawn_dvd()
                # ④ かご解放・強化
                elif 260 <= my <= 305 and self.basket_level < 5:
                    cost = self.get_basket_cost()
                    if self.score >= cost:
                        self.score -= cost
                        self.basket_level += 1
                
                self.canvas.itemconfig(self.score_text, text=f"ポイント: {self.score} pt")
                self.clear_menu()
                self.draw_menu()
                return

        p_radius = self.get_click_radius()

        #2点間の距離 <= (プレイヤーの判定半径 + オブジェクトの判定半径)

        #流れ星の判定
        if self.star is not None:
            distance = ((self.star["x"] - mx) ** 2 + (self.star["y"] - my) ** 2) ** 0.5
            if distance <= (p_radius + self.star["radius"]):
                self.score += 10000
                self.canvas.delete(self.star["id"])
                self.star = None
                self.canvas.itemconfig(self.score_text, text=f"ポイント: {self.score} pt")
                return

        #コインの判定
        for coin in self.coins[:]:
            distance = ((coin["x"] - mx) ** 2 + (coin["y"] - my) ** 2) ** 0.5
            if distance <= (p_radius + coin["radius"]):
                self.score += 100
                self.canvas.delete(coin["id"])
                self.coins.remove(coin)
                self.canvas.itemconfig(self.score_text, text=f"ポイント: {self.score} pt")
                break

    def game_loop(self):
        # コインの移動 & かごのキャッチ判定
        for coin in self.coins[:]:
            coin["y"] += coin["speed"]
            self.canvas.move(coin["id"], 0, coin["speed"])

            if self.basket_level > 0 and self.basket is not None:
                if (self.basket["y"] - 20 <= coin["y"] <= self.basket["y"] + 10) and (self.basket["x1"] <= coin["x"] <= self.basket["x2"]):
                    self.score += 100
                    self.canvas.delete(coin["id"])
                    self.coins.remove(coin)
                    self.canvas.itemconfig(self.score_text, text=f"ポイント: {self.score} pt")
                    continue

            if coin["y"] > 620:
                coin["x"] = random.randint(50, 750)
                coin["y"] = -40
                self.canvas.coords(coin["id"], coin["x"], coin["y"])

        # コインの総数調整
        while len(self.coins) < self.coin_level * 3:
            self.spawn_coin()

        # 全DVDの移動 & 壁バウンド判定
        for dvd in self.dvds:
            dvd["x"] += dvd["vx"]
            dvd["y"] += dvd["vy"]
            self.canvas.move(dvd["id"], dvd["vx"], dvd["vy"])

            hit = False
            if dvd["x"] < 20 or dvd["x"] > 780:
                dvd["vx"] *= -1
                hit = True
            if dvd["y"] < 20 or dvd["y"] > 580:
                dvd["vy"] *= -1
                hit = True

            if hit:
                self.score += self.dvd_level * 100
                self.canvas.itemconfig(self.score_text, text=f"ポイント: {self.score} pt")

        # 流れ星の移動 & 出現確率管理
        if self.star is not None:
            self.star["x"] += self.star["vx"]
            self.star["y"] += self.star["vy"]
            self.canvas.move(self.star["id"], self.star["vx"], self.star["vy"])
            
            if self.star["x"] < -50 or self.star["y"] > 650:
                self.canvas.delete(self.star["id"])
                self.star = None
        else:
            if random.random() < 0.002:
                self.spawn_shooting_star()

        self.root.after(16, self.game_loop)

if __name__ == "__main__":
    root = tk.Tk()
    app = UltimateClicker(root)
    root.mainloop()
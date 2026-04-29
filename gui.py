from PyQt5 import QtWidgets, QtCore, QtGui
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from weather_fetcher import WeatherFetcher

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Прогноз Погоды v1.0")
        self.setMinimumSize(900, 700)
        
        self.api_key = "56d9b439d22d4f65c796ec906c07a3b2" 
        self.fetcher = WeatherFetcher(self.api_key)
        
        self.setup_ui()
        self.apply_styles()
    
    def setup_ui(self):
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QVBoxLayout(central_widget)

        top_bar = QtWidgets.QHBoxLayout()
        self.city_input = QtWidgets.QLineEdit()
        self.city_input.setPlaceholderText("Введите город...")
        self.search_btn = QtWidgets.QPushButton("Узнать погоду")
        top_bar.addWidget(self.city_input)
        top_bar.addWidget(self.search_btn)
        layout.addLayout(top_bar)

        info_layout = QtWidgets.QHBoxLayout()
        self.today_lbl = QtWidgets.QLabel("[ СЕГОДНЯ ]\n--°C\n--")
        self.details_lbl = QtWidgets.QLabel("[ ДЕТАЛИ ]\nВлажность: --%\nВетер: -- м/с")
        info_layout.addWidget(self.today_lbl)
        info_layout.addWidget(self.details_lbl)
        layout.addLayout(info_layout)

        layout.addWidget(QtWidgets.QLabel("[ ПРОГНОЗ НА НЕДЕЛЮ ]"))
        self.week_layout = QtWidgets.QHBoxLayout()
        layout.addLayout(self.week_layout)

        layout.addWidget(QtWidgets.QLabel("[ ДИНАМИКА ТЕМПЕРАТУРЫ ]"))
        self.figure, self.ax = plt.subplots(figsize=(5, 3), tight_layout=True)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        self.search_btn.clicked.connect(self.on_search)

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow, QWidget { background-color: #1e1e1e; color: white; font-family: 'Segoe UI'; }
            QLineEdit { background-color: #2d2d2d; border: 1px solid #3d3d3d; padding: 8px; color: white; }
            QPushButton { background-color: #0078d4; font-weight: bold; padding: 8px 15px; border: none; }
            QLabel { font-size: 13px; }
        """)
        # Настройка графика под фото
        self.figure.patch.set_facecolor('#1e1e1e')
        self.ax.set_facecolor('#1e1e1e')
        self.ax.tick_params(colors='gray', labelsize=8)
        self.ax.grid(True, color='#333', linestyle='--')

    def on_search(self):
        city = self.city_input.text()
        if not city: return
        data = self.fetcher.get_weekly_forecast(city)
        if data and data.get("cod") == "200":
            self.update_display(data)

    def update_display(self, data):
        curr = data['list'][0]
        self.today_lbl.setText(f"[ СЕГОДНЯ ]\n{round(curr['main']['temp'])}°C\n{curr['weather'][0]['description']}")
        self.details_lbl.setText(f"[ ДЕТАЛИ ]\nВлажность: {curr['main']['humidity']}%\nВетер: {curr['wind']['speed']} м/с")

        for i in reversed(range(self.week_layout.count())): 
            self.week_layout.itemAt(i).widget().setParent(None)

        temps, dates = [], []
        for i in range(0, 40, 8):
            day = data['list'][i]
            d_str = day['dt_txt'][5:10]
            t = round(day['main']['temp'])
            dates.append(d_str)
            temps.append(t)
            
            card = QtWidgets.QLabel(f"{d_str}\n{t}°")
            card.setAlignment(QtCore.Qt.AlignCenter)
            card.setStyleSheet("background-color: #2d2d2d; border-radius: 5px; padding: 15px; font-size: 14px;")
            self.week_layout.addWidget(card)

        self.ax.clear()
        self.ax.plot(dates, temps, color='#00ced1', marker='o', linewidth=2)
        self.ax.fill_between(dates, temps, color='#00ced1', alpha=0.2)
        self.canvas.draw()

from PyQt5 import QtWidgets, QtCore, QtGui

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Визуализатор погоды на неделю")
        self.setMinimumSize(800, 600)
        self.setup_ui()
    
    def setup_ui(self):
        """Создание интерфейса"""
        # Центральный виджет
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной layout
        layout = QtWidgets.QVBoxLayout(central_widget)
        
        # Верхняя панель: ввод города и кнопка
        top_layout = QtWidgets.QHBoxLayout()
        
        self.city_input = QtWidgets.QLineEdit()
        self.city_input.setPlaceholderText("Введите город...")
        
        self.search_button = QtWidgets.QPushButton("Узнать погоду")
        
        top_layout.addWidget(self.city_input)
        top_layout.addWidget(self.search_button)
        
        # Область для вывода погоды (пока заглушка)
        self.weather_label = QtWidgets.QLabel("Здесь будет прогноз погоды")
        self.weather_label.setAlignment(QtCore.Qt.AlignCenter)
        self.weather_label.setStyleSheet("font-size: 14px; padding: 20px;")
        
        # Добавляем все в главный layout
        layout.addLayout(top_layout)
        layout.addWidget(self.weather_label)
        
        # Подключаем кнопку
        self.search_button.clicked.connect(self.on_search)
    
    def on_search(self):
        """Обработчик нажатия кнопки"""
        city = self.city_input.text()
        if city:
            self.weather_label.setText(f"Загрузка погоды для города: {city}...")
            # TODO: здесь будет вызов API
        else:
            self.weather_label.setText("Введите название города")

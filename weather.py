import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QPixmap

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")
        self.setGeometry(100, 100, 300, 400)

        # Layout
        layout = QVBoxLayout()

        # city
        self.city_input = QLineEdit(self)
        self.city_input.setPlaceholderText("Enter city name")
        layout.addWidget(self.city_input)

        # search button
        self.search_button = QPushButton("Get Weather", self)
        self.search_button.clicked.connect(self.get_weather)
        layout.addWidget(self.search_button)

        self.weather_label = QLabel("Weather info will appear here.", self)
        self.weather_label.setWordWrap(True)
        layout.addWidget(self.weather_label)

        self.icon_label = QLabel(self)
        layout.addWidget(self.icon_label)

        self.setLayout(layout)

    def get_weather(self):
        city = self.city_input.text()
        if not city:
            self.weather_label.setText("Please enter a city name.")
            return

       
        API_KEY = "72d644994d8d46efa0255259230605"
        url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"

        try:
            response = requests.get(url)
            data = response.json()

            if "error" in data:
                self.weather_label.setText(f"Error: {data['error']['message']}")
            else:
                temp = data['current']['temp_c']
                condition = data['current']['condition']['text']
                icon_url = "http:" + data['current']['condition']['icon']
                self.weather_label.setText(f"Temperature: {temp}°C\nCondition: {condition}")

                pixmap = QPixmap()
                pixmap.loadFromData(requests.get(icon_url).content)
                self.icon_label.setPixmap(pixmap)
        except Exception as e:
            self.weather_label.setText("Error fetching weather data.")
            print(e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())


![image](https://github.com/coinsspor/CryptoPricesWidget-/assets/38142283/680d5d82-dc75-48c2-a500-c7f09ed5fce4)


#ENGLISH
This Python script creates a desktop widget for monitoring cryptocurrency prices using the Tkinter library. It can be broadly categorized into three main functionalities: Main Widget Interface, Menu Options, and Alarm Functions.

Main Widget Interface:
Title: The window is titled "Crypto Prices Widget by coinsspor."
Background and Font Style: The background color is set to black with yellow font.
Default Values: Sets default values for refresh rate, font size, cryptocurrencies to be tracked (BTC and MINA), and alarm settings.
Price Display: Displays the current price of each cryptocurrency in USDT. Initially, BTC and MINA are tracked.
Menu Options:
Settings Menu:

Always on Top: An option to keep the widget always on top of other windows.
Set Refresh Rate: Allows users to set how often the prices will be updated.
Set Font Size: Provides the ability to change the font size of the text in the widget.
Manage Cryptos: Users can add or remove the cryptocurrencies they want to track.
Select Data Source: Option to choose the source of price information (Mexc, Binance, OKX, Kraken).
Alarm Menu:

Manage Alarms: Separate alarm settings for each cryptocurrency. Users can set upper and lower price limits.
Select Alarm Sound: Choose the sound that will play when the price reaches a certain limit.
Set Alarm Duration: Adjust how long the alarm sound will play.
Alarm Functions:
Alarms: Systems to alert the user when upper or lower limits are reached.
Sound Alerts: Playing selected sound files using Pygame.
Save Alarm Settings: Storing and applying the alarm settings as determined by the user.
Additional Features:
Price Updates: Automatically updates cryptocurrency prices at regular intervals from the selected data source.
Background Operations: Continuously operates in the background using the threading module. This allows the widget to regularly update prices and check for alarm conditions.
This script is a tool for those who want to keep track of the cryptocurrency market. With its user-friendly interface and extensive setting options, it is suitable for both beginners and experienced users alike.

#TURKISH
Bu Python betiği, Tkinter kütüphanesini kullanarak masaüstünde kripto para fiyatlarını takip eden bir widget oluşturur. İşlevleri genel olarak üç ana kategoriye ayrılabilir: Ana Widget Arayüzü, Menü Seçenekleri ve Alarm Fonksiyonları.

Ana Widget Arayüzü:
Başlık: "Crypto Prices Widget by coinsspor" olarak adlandırılmış bir pencere.
Arka Plan ve Yazı Stili: Arka plan rengi siyah ve yazı rengi sarı olarak ayarlanmış.
Varsayılan Değerler: Yenileme hızı, yazı boyutu, takip edilen kriptolar (BTC ve MINA) ve alarm ayarları için varsayılan değerler belirlenmiş.
Fiyat Görüntüleme: Her bir kripto para birimi için güncel fiyat, USDT cinsinden gösterilir. Başlangıçta BTC ve MINA takip edilir.
Menü Seçenekleri:
Ayarlar Menüsü:

Her Zaman Üstte Kalma: Widget'ın diğer pencerelerin önünde sabit kalmasını sağlayan bir seçenek.
Yenileme Hızını Ayarlama: Fiyatların kaç saniyede bir güncelleneceğini belirler.
Yazı Boyutunu Ayarlama: Widget'taki metinlerin boyutunu değiştirme imkanı sunar.
Kripto Para Birimlerini Yönetme: Kullanıcılar takip edilen kripto para birimlerini ekleyebilir veya çıkarabilirler.
Veri Kaynağı Seçme: Fiyat bilgilerinin alınacağı kaynağı seçme imkanı (Mexc, Binance, OKX, Kraken).
Alarm Menüsü:

Alarmları Yönetme: Her bir kripto para birimi için ayrı ayrı alarm ayarları. Üst ve alt fiyat limitleri belirlenebilir.
Alarm Sesi Seçimi: Fiyat belirli bir limite ulaştığında çalacak alarm sesini seçme.
Alarm Süresini Ayarlama: Alarm sesinin ne kadar süreyle çalacağını ayarlama.
Alarm Fonksiyonları:
Alarmlar: Üst ve alt limitlere ulaşıldığında kullanıcıyı uyaracak alarm sistemleri.
Sesli Uyarılar: Pygame kullanılarak belirlenen ses dosyalarının çalınması.
Alarm Ayarları Kaydetme: Kullanıcının belirlediği alarm ayarlarını saklama ve gerektiğinde uygulama.
Ekstra Özellikler:
Fiyat Güncellemesi: Seçilen veri kaynağından kripto para fiyatlarını düzenli aralıklarla otomatik olarak günceller.
Arka Plan İşlemleri: threading modülü sayesinde arka planda sürekli çalışan bir yapısı vardır. Bu, widget'ın fiyatları düzenli olarak güncellemesini ve alarm koşullarını kontrol etmesini sağlar.
Bu betik, kripto para piyasasını takip etmek isteyen kullanıcılara yönelik bir araçtır. Kullanıcı dostu arayüzü ve geniş ayar seçenekleri ile hem yeni başlayanlar hem de deneyimli kullanıcılar için uygundur.

[app]

# Uygulama Başlığı
title = Yulzak SMS Bomber

# Paket adı ve domain
package.name = sms_bomber
package.domain = com.yulzak

# Kaynak dizini ve dosya uzantıları
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# Uygulama sürümü
version = 1.0

# Gerekli Python paketleri
requirements = python3,kivy,requests,colorama,pyjnius==1.6.1

# Ekran yönü
orientation = portrait

# İkon ve presplash
icon.filename = uyg.png
presplash.filename = arkaplan.png

# Android izinleri
android.permissions = INTERNET

# Uygulama tam ekran olsun
fullscreen = 1

# Android mimarileri
android.archs = arm64-v8a, armeabi-v7a

# Auto backup açık
android.allow_backup = True

# Log seviyesi debug
[buildozer]
log_level = 2
warn_on_root = 1

# Bin klasörü
bin_dir = ./bin

"""
DevSecOps Pipeline Demo - KASITLI GÜVENLİK AÇIĞI İÇEREN KOD
==============================================================
⚠️ UYARI: Bu dosya SADECE demo amaçlıdır!
Pipeline'ın güvenlik açıklarını yakalayabildiğini göstermek için yazılmıştır.
Gerçek projelerde bu tarz kod ASLA kullanılmamalıdır!

Bandit bu dosyada şu açıkları bulacaktır:
- B105: Hardcoded password (koda gömülmüş şifre)
- B301: Pickle kullanımı (güvensiz deserialization)
- B303: MD5 kullanımı (güvensiz hash)
- B602: subprocess shell=True (komut enjeksiyonu riski)
- B608: SQL Injection (SQL enjeksiyonu)
"""

import os
import pickle
import hashlib
import subprocess


# ❌ B105 - HARDCODED PASSWORD
# Şifreler asla kodun içine yazılmamalı!
# Doğrusu: os.environ.get("DB_PASSWORD")
DATABASE_PASSWORD = "super_secret_password_123"
API_KEY = "sk-proj-abc123def456ghi789"


def guvensizhash(parola):
    """
    ❌ B303 - GÜVENSIZ HASH FONKSİYONU
    MD5, kriptografik olarak kırılmıştır. Parola hashlemek için kullanılmamalı.
    Doğrusu: hashlib.sha256() veya hashlib.pbkdf2_hmac()
    """
    return hashlib.md5(parola.encode()).hexdigest()


def tehlikeli_komut_calistir(kullanici_girdisi):
    """
    ❌ B602 - SHELL INJECTION
    Kullanıcı girdisi doğrudan shell komutuna geçirilirse,
    saldırgan kendi komutlarını çalıştırabilir.
    Örn: kullanici_girdisi = "dosya.txt; rm -rf /"
    Doğrusu: subprocess.run(["ls", "-la", safe_path], shell=False)
    """
    subprocess.call("ls -la " + kullanici_girdisi, shell=True)


def guvensiz_veri_yukle(dosya_yolu):
    """
    ❌ B301 - GÜVENSIZ DESERIALIZATION
    pickle.load() güvenilmeyen kaynaklardan veri yüklerken
    keyfi kod çalıştırılmasına izin verebilir.
    Doğrusu: json.load() kullanmak
    """
    with open(dosya_yolu, "rb") as f:
        return pickle.load(f)


def guvensiz_sorgu(kullanici_id):
    """
    ❌ B608 - SQL INJECTION
    Kullanıcı girdisi doğrudan SQL sorgusuna eklenirse,
    saldırgan veritabanını manipüle edebilir.
    Örn: kullanici_id = "1 OR 1=1; DROP TABLE users;--"
    Doğrusu: cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    """
    query = "SELECT * FROM kullanicilar WHERE id = " + kullanici_id
    return query

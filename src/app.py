"""
DevSecOps Pipeline Demo - Ana Uygulama
=======================================
Bu dosya güvenli kod yazım pratiklerini göstermek için hazırlanmıştır.
Tüm güvenlik kurallarına uygun, Bandit taramasından geçebilen koddur.
"""

import os
import hashlib
import logging
from flask import Flask, request, jsonify

# Loglama yapılandırması
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route("/")
def home():
    """Ana sayfa - API bilgilerini döndürür."""
    return jsonify({
        "uygulama": "DevSecOps Pipeline Demo",
        "versiyon": "1.0.0",
        "durum": "calisiyor",
        "aciklama": "Guvenli yazilim gelistirme hatti demo uygulamasi"
    })


@app.route("/hash", methods=["POST"])
def hash_data():
    """
    Güvenli hash fonksiyonu kullanımı.
    SHA-256 kullanır (MD5 veya SHA-1 değil - bunlar güvensiz).
    """
    data = request.get_json()

    if not data or "text" not in data:
        logger.warning("Hash isteginde 'text' alani eksik")
        return jsonify({"hata": "'text' alani zorunludur"}), 400

    text = data["text"]

    # ✅ GÜVENLI: SHA-256 kullanıyoruz (Bandit B303 - md5/sha1 kullanmıyoruz)
    hashed = hashlib.sha256(text.encode("utf-8")).hexdigest()

    logger.info("Hash basariyla olusturuldu")
    return jsonify({
        "orijinal_uzunluk": len(text),
        "hash_algoritmasi": "SHA-256",
        "hash": hashed
    })


@app.route("/config")
def get_config():
    """
    Konfigürasyonu ortam değişkenlerinden alır.
    Şifreleri/anahtarları ASLA koda gömmüyoruz (hardcode).
    """
    # ✅ GÜVENLI: Ortam değişkenlerinden okuyoruz (Bandit B105 - hardcoded password yok)
    config = {
        "db_host": os.environ.get("DB_HOST", "localhost"),
        "db_port": os.environ.get("DB_PORT", "5432"),
        "db_name": os.environ.get("DB_NAME", "demo_db"),
        "debug_mode": os.environ.get("DEBUG", "false").lower() == "true"
    }

    logger.info("Konfigurasyon bilgileri istendi")
    return jsonify(config)


@app.route("/health")
def health_check():
    """Sağlık kontrolü endpoint'i - Uygulamanın çalıştığını doğrular."""
    return jsonify({
        "durum": "saglikli",
        "kontroller": {
            "uygulama": "calistiyor",
            "python_versiyon": os.sys.version
        }
    })


if __name__ == "__main__":
    # ✅ GÜVENLI: 0.0.0.0 yerine 127.0.0.1 kullanıyoruz (Bandit B104)
    # ✅ GÜVENLI: debug=False (production'da debug açık olmamalı)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="127.0.0.1", port=port, debug=False)

# 🔒 DevSecOps Pipeline — Güvenli Yazılım Geliştirme Hattı

[![🔒 DevSecOps Güvenlik Hattı](https://github.com/EmirKaraarslan35/devsecops-pipeline/actions/workflows/security-pipeline.yml/badge.svg)](https://github.com/EmirKaraarslan35/devsecops-pipeline/actions/workflows/security-pipeline.yml)
[![🔍 SAST - Bandit Güvenlik Taraması](https://github.com/EmirKaraarslan35/devsecops-pipeline/actions/workflows/sast-bandit.yml/badge.svg)](https://github.com/EmirKaraarslan35/devsecops-pipeline/actions/workflows/sast-bandit.yml)
[![📦 Bağımlılık Güvenlik Kontrolü](https://github.com/EmirKaraarslan35/devsecops-pipeline/actions/workflows/dependency-check.yml/badge.svg)](https://github.com/EmirKaraarslan35/devsecops-pipeline/actions/workflows/dependency-check.yml)

---

## 📌 Proje Hakkında

Bu proje, yazılım geliştirme sürecine güvenliği entegre eden bir **DevSecOps (Development + Security + Operations)** boru hattı (pipeline) implementasyonudur.

Kod her commit edildiğinde, açık kaynaklı güvenlik araçları otomatik olarak çalışır ve güvenlik açığı tespit edildiğinde süreç durdurularak güvenli olmayan kodun canlı ortama çıkması engellenir.

### 🎯 Amaç

> Güvenlik testlerinden geçmeyen kodun canlıya çıkmasını engelleyen **otomatik bir boru hattı** kurmak.

---

## 🏗️ Pipeline Mimarisi

```
                    ┌─────────────────┐
                    │   git push /    │
                    │  Pull Request   │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
     ┌────────────┐ ┌────────────┐ ┌────────────┐
     │  🔍 SAST   │ │  📦 Dep.   │ │  🔑 Secret │
     │  Bandit    │ │  pip-audit │ │  Gitleaks  │
     │  Kod       │ │  Kütüphane │ │  Şifre/Key │
     │  Taraması  │ │  Taraması  │ │  Taraması  │
     └─────┬──────┘ └─────┬──────┘ └─────┬──────┘
           │              │              │
           └──────────────┼──────────────┘
                          │
                          ▼
                 ┌────────────────┐
                 │  🚦 Güvenlik   │
                 │    Kapısı      │
                 │  (Hepsi ✅?)   │
                 └───────┬────────┘
                         │
              ┌──────────┴──────────┐
              │                     │
              ▼                     ▼
     ┌────────────────┐    ┌────────────────┐
     │ ✅ Deploy       │    │ ❌ ENGELLE     │
     │ Canlıya Al      │    │ Kod Canlıya    │
     │                 │    │ ÇIKAMAZ        │
     └────────────────┘    └────────────────┘
```

---

## 🛡️ Güvenlik Araçları

### 1. 🔍 Bandit — Statik Uygulama Güvenlik Testi (SAST)

Python kaynak kodunu çalıştırmadan analiz ederek güvenlik açıklarını tespit eder.

| Tespit Edilen Açık Türleri | Bandit Test ID |
|---|---|
| Koda gömülü şifreler (Hardcoded Passwords) | B105 |
| Güvensiz hash fonksiyonları (MD5, SHA-1) | B303, B324 |
| Shell enjeksiyonu (Command Injection) | B602 |
| SQL enjeksiyonu (SQL Injection) | B608 |
| Güvensiz deserialization (Pickle) | B301 |
| Tüm arayüzlere bağlanma (0.0.0.0) | B104 |

### 2. 📦 pip-audit — Bağımlılık Güvenlik Kontrolü

`requirements.txt` dosyasındaki Python kütüphanelerini [PyPI Advisory Database](https://github.com/pypa/advisory-database) ile karşılaştırarak bilinen güvenlik açıklarını (CVE) tespit eder.

### 3. 🛡️ OWASP Dependency-Check — Kapsamlı Bağımlılık Taraması

Projedeki tüm bağımlılıkları **NVD (National Vulnerability Database)** ile karşılaştırarak bilinen güvenlik açıklarını (CVE) tespit eder. CVSS puanı 7.0 ve üzeri olan açıklar bulunduğunda pipeline durdurulur.

### 4. 🔑 Gitleaks — Gizli Bilgi Taraması (Secret Scanning)

Git geçmişi dahil tüm commit'lerde yanlışlıkla bırakılmış şifreleri, API anahtarlarını, token'ları ve diğer gizli bilgileri tespit eder.

### 5. 🖥️ SonarQube — Kapsamlı Kod Kalitesi ve Güvenlik Analizi

30'dan fazla programlama dilini destekleyen, kod kalitesi (code smell, duplicate code) ve güvenlik açıklarını analiz eden platform. Quality Gate ile kodun belirlenen kalite standartlarını karşılayıp karşılamadığını kontrol eder.

### 6. 🧪 pytest — Birim Testleri

Python kodunun doğru çalıştığını doğrulayan otomatik testler. Kod kapsamı (coverage) raporu üretir.

---

## 📁 Proje Yapısı

```
devsecops-pipeline/
├── .github/
│   └── workflows/
│       ├── security-pipeline.yml    # Birleşik güvenlik hattı
│       ├── sast-bandit.yml          # SAST taraması (bağımsız)
│       └── dependency-check.yml     # Bağımlılık kontrolü (bağımsız)
├── src/
│   ├── __init__.py
│   ├── app.py                       # Ana uygulama (güvenli kod)
│   └── vulnerable_demo.py.bak      # Demo: güvenlik açığı örnekleri
├── tests/
│   └── test_app.py                  # Birim testleri
├── requirements.txt                 # Python bağımlılıkları
├── .bandit                          # Bandit konfigürasyonu
├── .gitleaks.toml                   # Gitleaks konfigürasyonu
├── sonar-project.properties         # SonarQube konfigürasyonu
├── .gitignore                       # Git hariç tutma listesi
└── README.md                        # Bu dosya
```

---

## 🚀 Kurulum ve Kullanım

### Gereksinimler

- Python 3.10+
- Git
- GitHub hesabı

### Yerel Kurulum

```bash
# 1. Repoyu klonla
git clone https://github.com/EmirKaraarslan35/devsecops-pipeline.git
cd devsecops-pipeline

# 2. Bağımlılıkları kur
pip install -r requirements.txt

# 3. Güvenlik araçlarını kur
pip install bandit pip-audit

# 4. Uygulamayı çalıştır
python -m src.app
```

### Güvenlik Taramalarını Yerel Olarak Çalıştırma

```bash
# SAST taraması (Bandit)
bandit -r src/ -f screen

# Bağımlılık kontrolü (pip-audit)
pip-audit -r requirements.txt --desc

# Testleri çalıştır
pip install pytest
pytest tests/ -v
```

---

## 🧪 Demo Senaryoları

### Senaryo 1: Güvenlik Açığı Olan Kod (Pipeline DURUR ❌)

`src/vulnerable_demo.py.bak` dosyasındaki açıklı kodu `src/` klasörüne `.py` uzantısıyla eklerseniz, pipeline aşağıdaki açıkları tespit edip duracaktır:

- ❌ **B105:** Koda gömülü şifre (`DATABASE_PASSWORD = "super_secret_123"`)
- ❌ **B324:** Güvensiz MD5 hash kullanımı
- ❌ **B602:** Shell injection riski (`shell=True`)
- ❌ **B301:** Güvensiz `pickle.load()` kullanımı
- ❌ **B608:** SQL Injection riski

### Senaryo 2: Güvenli Kod (Pipeline GEÇER ✅)

`src/app.py` dosyası tüm güvenlik kurallarına uygun yazılmıştır:

- ✅ Şifreler ortam değişkenlerinden okunuyor
- ✅ SHA-256 güvenli hash kullanılıyor
- ✅ `127.0.0.1` ile bağlanılıyor (tüm arayüzlere açılmıyor)
- ✅ `debug=False` production ayarı

---

## 📊 OWASP Top 10 Kapsamı

| # | OWASP Kategorisi | Karşılayan Araç |
|---|---|---|
| A02 | Cryptographic Failures | Bandit (B303, B324) |
| A03 | Injection | Bandit (B602, B608) |
| A05 | Security Misconfiguration | Bandit (B104) |
| A06 | Vulnerable Components | pip-audit |
| A08 | Software & Data Integrity Failures | Bandit (B301) |
| A09 | Security Logging & Monitoring | Gitleaks |

---

## 📚 Kullanılan Teknolojiler

| Teknoloji | Açıklama | Versiyon |
|---|---|---|
| [Python](https://python.org) | Programlama dili | 3.12 |
| [Flask](https://flask.palletsprojects.com) | Web framework | 3.1.3 |
| [Bandit](https://bandit.readthedocs.io) | SAST aracı | 1.9+ |
| [pip-audit](https://github.com/pypa/pip-audit) | Bağımlılık kontrolü | 2.10+ |
| [Gitleaks](https://github.com/gitleaks/gitleaks) | Secret scanning | Latest |
| [GitHub Actions](https://docs.github.com/actions) | CI/CD platformu | v4 |

---

## 📝 Lisans

Bu proje eğitim amaçlı hazırlanmıştır.

---

## 👤 Geliştirici

**Emir Karaarslan** — [GitHub](https://github.com/EmirKaraarslan35)

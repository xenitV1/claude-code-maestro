# Maestro: Yapay Zeka Geliştirme Orkestratörü

Claude Code CLI için elit seviye orkestrasyon çerçevesi. Özelleşmiş ajanlar, modüler beceriler, akıllı hook sistemi ve kalıcı bellek sistemleri aracılığıyla yapay zeka geliştirmeyi güçlendirir.

> **Versiyon:** 0.6.0  
> **Yazar:** [xenitV1](https://github.com/xenitV1) • [X/Twitter](https://x.com/xenit_v0)  
> **Felsefe:** "Nasıl'dan önce Neden. Mimari, uygulamadan önce gelir."

## Hızlı Başlangıç

### Kurulum

Maestro bir Claude Code eklentisi (plugin) olarak dağıtılır. Kurmak için önce repoyu bir "marketplace" olarak eklemeniz gerekir:

```bash
# 1. Maestro reposunu marketplace olarak ekleyin
/plugin marketplace add xenitV1/claude-code-maestro

# 2. Maestro eklentisini kurun
/plugin install maestro@xenitV1-claude-code-maestro
```

### Önkoşullar

- **Node.js 18+** (hook sistemi için gereklidir)
- Claude Code CLI

### Kullanım

Maestro bir eklenti (plugin) olduğu için komutları isim alanı (namespace) gerektirir. `/maestro:komut` formatını kullanın.

```bash
# Basic orchestration
/maestro your task description

# With Ralph Wiggum (autonomous iterations)
/maestro fix bugs and improve code. ralph 5 iterations

# Design mode
/maestro design new authentication system

# Plan mode
/maestro plan implement user dashboard

# Use the Grandmaster agent directly
/agent:grandmaster
```

## Mimari

```
┌─────────────────────────────────────────────────────────────────────┐
│                         MAESTRO SİSTEMİ                              │
├─────────────────────────────────────────────────────────────────────┤
│  ┌──────────┐    ┌──────────────┐    ┌─────────────────────────┐   │
│  │ /maestro │───▶│ grandmaster  │───▶│       BECERİLER         │   │
│  │  komutu  │    │    ajanı      │    │ (frontend, backend,     │   │
│  └──────────┘    └──────────────┘    │  tdd, debug, vb.)       │   │
│                         │            └─────────────────────────┘   │
│                         ▼                                           │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    HOOK SİSTEMİ                              │   │
│  │  SessionStart │ PostToolUse │ Stop │ PreCompact │ vb.       │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                         │                                           │
│                         ▼                                           │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                   UZUN SÜRELİ BELLEK (LTM)                    │   │
│  │                      (brain.jsonl)                            │   │
│  └──────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Proje Yapısı

```
maestro/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifestosu
├── agents/
│   └── grandmaster.md       # Merkezi orkestratör ajan
├── commands/
│   └── maestro.md           # /maestro slash komutu
├── hooks/
│   ├── hooks.json           # Hook konfigürasyonu
│   ├── lib/                 # Paylaşılan JS yardımcıları
│   │   ├── utils.js         # Platformlar arası yardımcılar
│   │   ├── brain.js         # LTM işlemleri
│   │   └── ralph.js         # Ralph durum yönetimi
│   ├── session-start.js     # Tech stack tespiti + LTM enjeksiyonu
│   ├── brain-sync.js        # LTM senkronizasyonu (PostToolUse)
│   ├── stop.js              # Ralph Wiggum iterasyonu
│   ├── ralph.js             # QA zorlaması
│   ├── sentinel.js          # Değişiklik algılama
│   └── pre-maestro.js       # Beceri önerisi
├── skills/
│   ├── clean-code/          # Kod kalite standartları
│   ├── frontend-design/     # Elit UI/UX
│   ├── backend-design/      # API & Veritabanı kalıpları
│   ├── tdd-mastery/         # Test Odaklı Geliştirme
│   ├── debug-mastery/       # Sistematik hata ayıklama
│   ├── verification-mastery/# Kanıt tabanlı tamamlama
│   ├── brainstorming/       # Tasarım öncelikli metodoloji
│   ├── planning-mastery/    # Uygulama planlama
│   ├── git-worktrees/       # İzole çalışma alanları
│   ├── ralph-wiggum/        # Otonom QA sistemi
│   ├── browser-extension/   # Tarayıcı eklentisi geliştirme
│   └── optimization-mastery/# Performans optimizasyonu
├── package.json             # Node.js meta verileri
├── LICENSE                  # MIT Lisansı
└── README.md
```

## Bellek Sistemleri

### Uzun Süreli Bellek (brain.jsonl)
Oturumlar arası kalıcı proje bağlamı:
- **Tech Stack:** Framework'ler, bağımlılıklar, mimari kalıplar
- **Kararlar:** Alınan önemli mimari kararlar
- **Hedefler:** Proje amaçları
- **Hatalar:** Bilinen sorunlar ve engelleyiciler
- **Compact Geçmişi:** Context sıkıştırması sonrası oturum özetleri
- **Dosya Değişiklikleri:** Edit ve Create işlemlerinin kaydı

## Ralph Wiggum: Otonom QA

Dört Sütunlu Elit QA Sistemi:

| Sütun | Amaç |
|-------|------|
| **Proactive Gate** | Kodlamadan ÖNCE kenar durum tespiti |
| **Reflection Loop** | Öz-eleştiri ve iyileştirme |
| **Verification Matrix** | Test kapsama takibi (minimum %80) |
| **Circuit Breaker** | Duraksama tespiti ve pivot stratejileri |

Aktifleştirme: `ralph N iterasyon` veya "Ralph Wiggum modu"

## Becerilere Genel Bakış

| Beceri | Açıklama |
|--------|----------|
| `clean-code` | 2025 standartları, SOLID, güvenlik öncelikli |
| `frontend-design` | Atomic Design 2.0, Lovable/v0 standardı |
| `backend-design` | Zero-trust, API sözleşmeleri |
| `tdd-mastery` | Demir Yasa: Koddan önce test |
| `debug-mastery` | 4 fazlı sistematik hata ayıklama |
| `verification-mastery` | Tamamlamadan önce kanıt |
| `brainstorming` | Tasarım öncelikli metodoloji |
| `planning-mastery` | Küçük parçalı görev kırılımı |
| `git-worktrees` | İzole özellik geliştirme |
| `ralph-wiggum` | Otonom QA orkestrasyonu |
| `optimization-mastery` | Performans, INP, kısmi hidrasyon |
| `context7` | Upstash üzerinden otomatik kütüphane dokümantasyonu |
| `browser-extension` | Manifest v3, servis çalışanları |

## Platform Uyumluluğu

| Platform | Puan | Notlar |
|----------|------|--------|
| **Claude Code CLI** | ⭐⭐⭐⭐⭐ | Doğal ortam, tam işlevsellik |
| **Windows** | ⭐⭐⭐⭐⭐ | Tam platformlar arası destek |
| **macOS** | ⭐⭐⭐⭐⭐ | Tam platformlar arası destek |
| **Linux** | ⭐⭐⭐⭐⭐ | Tam platformlar arası destek |

## Çekirdek Protokoller

1. **Sokratik Geçit:** Varsaymadan önce netleştirici sorular sor
2. **Önce Düşün:** Karmaşık eylemlerden önce `<think>` kullan
3. **TDD Demir Yasası:** Başarısız test olmadan üretim kodu yok
4. **Doğrulama:** Tamamlama iddialarından önce kanıt
5. **Temiz Kod:** TODO/FIXME yok, tembel placeholder yok

## Teşekkür

Birçok beceri [obra/superpowers](https://github.com/obra/superpowers) projesinden ilham alınarak adapte edilmiş ve Maestro orkestrasyon ortamı için ağır bir şekilde optimize edilmiştir:

| Özellik | Kaynak | Maestro Becerisi |
|---------|--------|------------------|
| TDD Demir Yasası | superpowers/tdd | `tdd-mastery` |
| Sistematik Hata Ayıklama | superpowers/debugging | `debug-mastery` |
| Doğrulama Protokolü | superpowers/verification | `verification-mastery` |
| Beyin Fırtınası Metodu | superpowers/brainstorming | `brainstorming` |
| Uygulama Planlama | superpowers/planning | `planning-mastery` |
| Git Worktrees | superpowers/worktrees | `git-worktrees` |

## Yıldız Geçmişi

[![Star History Chart](https://api.star-history.com/svg?repos=xenitV1/claude-code-maestro&type=Date)](https://star-history.com/#xenitV1/claude-code-maestro&Date)

## Yazar

**[xenitV1](https://github.com/xenitV1)** tarafından oluşturuldu ve sürdürülüyor.

- GitHub: [github.com/xenitV1](https://github.com/xenitV1)
- X/Twitter: [x.com/xenit_v0](https://x.com/xenit_v0)

## Lisans

MIT Lisansı - Detaylar için [LICENSE](LICENSE) dosyasına bakınız.

---

*Otonom geliştirmenin geleceğini orkestre ediyoruz.*

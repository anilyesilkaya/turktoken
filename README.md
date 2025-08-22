# TurkToken

TurkToken, **Türkçe için özel olarak geliştirilmiş bir tokenizasyon kütüphanesi ve demo uygulamasıdır**.  
Amaç, Türkçenin eklemeli (agglutinative) yapısına daha uygun çözümler sunarak, dil işleme çalışmalarında kullanılan token sayılarını azaltmak, nadir kelimelerle (OOV) daha iyi başa çıkmak ve dil modelleri için daha verimli bir altyapı oluşturmaktır.

<p align="center">
  <img src="assets/cover.png" alt="TurkToken" width="450">
</p>

---

## 🚀 Özellikler

- **Farklı tokenizasyon modları:**
  - [**An itibariyle geliştirilmekte**] Karakter tabanlı
  - [**An itibariyle geliştirilmekte**] Kelime tabanlı
  - [Yakın zamanda başlanacak]          Alt-kelime tabanlı (BPE)
- **Türkçe’ye özgü zorluklara çözüm:**
  - Türkçe karakterlerin (ç, ğ, ı, İ, ö, ş, ü) korunması
  - Kesme işaretinin (`’` `'`) tutarlı biçimde işlenmesi
  - Ek sınırlarında daha doğru parçalama
- **Karşılaştırma imkânı:** SentencePiece ve WordPiece gibi yöntemlerle kıyaslama
- **Web demo:** Tarayıcı tabanlı, renkli token gösterimi ve hız ölçümleri

---

## 📦 Kurulum

Projeyi bilgisayarınıza klonlayın:

```bash
git clone https://github.com/kullanici/turktoken.git
cd turktoken
```

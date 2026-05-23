import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def site_kontrol(url, aranacak_yazi, bekleme_suresi):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        while True:
            try:
                print(f"\n[{url}] kontrol ediliyor...")
                await page.goto(url, timeout=60000)
                html = await page.content()
                soup = BeautifulSoup(html, "html.parser")
                sayfa_metni = soup.get_text(separator=" ")
                temiz_metin = sayfa_metni.lower()

                if aranacak_yazi.lower() in temiz_metin:
                    print("\nBULUNDU!")
                    print(f"Aranan yazı bulundu: {aranacak_yazi}")
                    # Bildirim sistemi gelecek
                    break
                else:
                    print("Henüz bulunamadı.")

            except Exception as hata:
                print("Hata oluştu:", hata)

            print(f"{bekleme_suresi} saniye bekleniyor...")
            await asyncio.sleep(bekleme_suresi)

        await browser.close()

if __name__ == "__main__":
    print("--- PagePulse Başlatılıyor ---\n")
    
    hedef_url = input("URL gir: ").strip()
    aranan = input("Aranacak yazı: ").strip()
    
    while True:
        try:
            sure_input = input("Kaç saniyede bir kontrol edilsin (örn: 30): ")
            sure = int(sure_input)
            
            if sure < 5:
                print("Çok kısa süre girdiniz. Engellenmemek için en az 5 saniye olarak ayarlanıyor.")
                sure = 5
                
            break
        except ValueError:
            print("Lütfen sadece rakam girin!")

    try:
        asyncio.run(site_kontrol(hedef_url, aranan, sure))
    except KeyboardInterrupt:
        print("\nProgram kullanıcı tarafından durduruldu (CTRL+C).")
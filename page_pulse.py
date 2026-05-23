import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

URL = "https://example.com"
ARANACAK_YAZI = "in stock"

async def site_kontrol():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        page = await browser.new_page()

        while True:
            try:
                print("\nSite kontrol ediliyor...")

                await page.goto(URL, timeout=60000)

                html = await page.content()

                soup = BeautifulSoup(html, "html.parser")

                sayfa_metni = soup.get_text(separator=" ")

                temiz_metin = sayfa_metni.lower()

                if ARANACAK_YAZI.lower() in temiz_metin:
                    print("\nBULUNDU!")
                    print(f"Aranan yazı bulundu: {ARANACAK_YAZI}")

                    # Bildirim sistemi gelecek

                    break

                else:
                    print("Henüz bulunamadı.")

            except Exception as hata:
                print("Hata oluştu:", hata)

            print("30 saniye bekleniyor...")
            await asyncio.sleep(30)

        await browser.close()

asyncio.run(site_kontrol())
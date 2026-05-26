import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
from datetime import datetime
from plyer import notification

# Colorama başlat
init(autoreset=True)

LOG_DOSYASI = "log.txt"

def log_yaz(mesaj):
    
    zaman = datetime.now().strftime("%H:%M:%S")

    with open(LOG_DOSYASI, "a", encoding="utf-8") as dosya:
        dosya.write(f"[{zaman}] {mesaj}\n")

def bildirim_gonder(baslik, mesaj):
    notification.notify(
        title=baslik,
        message=mesaj,
        timeout=10
    )

async def site_kontrol(url, aranacak_yazi, bekleme_suresi):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        page = await browser.new_page()

        while True:
            try:
                print(Fore.CYAN + f"\n[{url}] kontrol ediliyor...")

                log_yaz(f"{url} kontrol edildi")

                await page.goto(url, timeout=60000)

                html = await page.content()

                soup = BeautifulSoup(html, "html.parser")

                sayfa_metni = soup.get_text(separator=" ")

                temiz_metin = sayfa_metni.lower()

                if aranacak_yazi.lower() in temiz_metin:

                    print(Fore.GREEN + "\nBULUNDU!")

                    print(
                        Fore.GREEN +
                        f"Aranan yazı bulundu: {aranacak_yazi}"
                    )

                    bildirim_gonder(
                    "PagePulse Alert",
                    f'"{aranacak_yazi}" bulundu!'
)
                    log_yaz(
                        f"Aranan yazı bulundu: {aranacak_yazi}"
                    )

                    break

                else:
                    print(Fore.YELLOW + "Henüz bulunamadı.")

                    log_yaz("Henüz bulunamadı")

            except Exception as hata:

                print(Fore.RED + f"Hata oluştu: {hata}")

                log_yaz(f"Hata oluştu: {hata}")

            print(
                Fore.MAGENTA +
                f"{bekleme_suresi} saniye bekleniyor..."
            )

            await asyncio.sleep(bekleme_suresi)

        await browser.close()

if __name__ == "__main__":

    print(
        Fore.BLUE +
        Style.BRIGHT +
        "--- PagePulse Başlatılıyor ---\n"
    )

    hedef_url = input("URL gir: ").strip()

    aranan = input("Aranacak yazı: ").strip()

    while True:
        try:
            sure_input = input(
                "Kaç saniyede bir kontrol edilsin (örn: 30): "
            )

            sure = int(sure_input)

            if sure < 5:
                print(
                    Fore.YELLOW +
                    "Çok kısa süre girdiniz. "
                    "En az 5 saniye ayarlanıyor."
                )

                sure = 5

            break

        except ValueError:
            print(
                Fore.RED +
                "Lütfen sadece rakam girin!"
            )

    try:
        asyncio.run(
            site_kontrol(
                hedef_url,
                aranan,
                sure
            )
        )

    except KeyboardInterrupt:

        print(
            Fore.RED +
            "\nProgram kullanıcı tarafından durduruldu."
        )

        log_yaz("Program kullanıcı tarafından durduruldu")
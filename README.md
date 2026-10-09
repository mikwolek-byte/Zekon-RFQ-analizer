# Zekon RFQ 1.0 — analiza zapytań i karta wymagań

Kompletna aplikacja offline w jednym pliku `zekon_rfq.py`. Interfejs Tkinter,
dwa pakiety zewnętrzne do dokumentów. Logo Zekon osadzono w kodzie na podstawie
przekazanego wzoru oferty. Nie wymaga dostępu do internetu ani klucza API podczas pracy.

## Proces i dane wejściowe

Program realizuje uzgodniony proces Zekon: wczytanie materiałów → znalezienie
fragmentów → przegląd i potwierdzenie → karta wymagań → raport XLSX i HTML.
Projekt, klient i numer/rewizja są wprowadzane ręcznie, aby nie pomylić danych
zapytania, inwestora i dokumentów wzorcowych. Puste pola raportu: „Do wyjaśnienia”.

Karta obejmuje: zakres i ilości; gabaryty; EN 1090 i EXC; materiały i atesty;
spawanie; antykorozję i ochronę ogniową; tolerancje; kontrolę; dokumentację;
pakowanie i transport; terminy. Zachowuje oryginalne zapisy i wydania norm.
Nie przyjmuje automatycznie norm aktualnych ani domyślnych klas, gatunków i procentów NDT.

Dodatkowe uwagi PL/DE/EN/FR: NELSON i Kopfbolzen, przeciwstrzałka/Überhöhung/camber/
contre-flèche, osobno ugięcie/deflection/Durchbiegung/flèche, gwinty, odwodnienia,
stal nierdzewna, PRS/IW/HWS/IKS, S275/S420/S460/S690, słupy krzyżowe, frezowanie,
powierzchnie kontaktowe i dociskowe. Reguły `RULES` i `SPECIAL` w kodzie można rozszerzać.
Dopasowania są regułowe, nie stanowią tłumaczenia ani analizy semantycznej przez AI.

## Obsługiwane formaty

- PDF: warstwa tekstowa, tekst adnotacji, wartości interaktywnych formularzy.
- XLSX/XLSM: treść komórek wszystkich arkuszy, także ukrytych. Formuły pokazane
  jako tekst; makra i formuły NIE są wykonywane ani przeliczane.
- DOCX: tekst dokumentu, tabel, nagłówków i stopek; wybrane checkboxy Word.
  Źródło wskazuje część XML i wiersz, nie numer strony Word.
- TXT/CSV: tekst; próba UTF-8, UTF-16, Windows-1250/1252.
- IFC: właściwości tekstowe STEP i nazwy materiałów. Bez geometrii, korelacji
  materiał–element, wyznaczania BOM czy masy. Materiały modelu mogą dotyczyć
  całego projektu; użytkownik musi sprawdzić przypisanie i zakres Zekon.
- ZIP: dokumenty odczytywane wewnątrz paczki bez zapisywania plików na dysku.
  Pliki o identycznej zawartości wykrywane przez SHA256.

RAR/7z, DWG/DXF, XLS, JPG/PNG i zagnieżdżone ZIP nie są odczytywane. Są wymieniane
w spisie jako nieprzeanalizowane. RAR zamień na ZIP, DWG eksportuj do PDF.
Skany wymagają zewnętrznego OCR; program zgłasza strony ze zbyt małą warstwą tekstową.
Nie interpretujemy graficznych symboli spoin, geometrii, wymiarów bez tekstu,
zdjęć, rysunków osadzonych w Wordzie ani zaznaczeń graficznych w skanowanych formularzach.
Znaleziony tekst formularza zawsze wymaga przeglądu wizualnego. Słowo obok pustej
kratki nie staje się automatycznie obowiązującym wymaganiem.

## Instalacja Windows 10/11

1. Zainstaluj Python 3.10 lub nowszy w standardowej dystrybucji z tkinter.
   Rekomendowana wersja do pierwszego wdrożenia: Python 3.12 x64.
2. Rozpakuj cały pakiet do osobnego folderu.
3. Dwuklik `URUCHOM.bat` tworzy środowisko, instaluje pakiety i uruchamia program.
   Pierwsza instalacja wymaga internetu.

Albo w PowerShell / terminalu otwartym w folderze aplikacji:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe zekon_rfq.py
```

## Samodzielny Windows EXE

Dwuklik `BUDUJ_EXE.bat` albo:

```powershell
.\.venv\Scripts\python.exe -m pip install "pyinstaller>=6.16,<7"
.\.venv\Scripts\python.exe -m PyInstaller --clean --noconfirm --onefile --windowed --name Zekon_RFQ zekon_rfq.py
```

Wynik: `dist\Zekon_RFQ.exe`. Logo jest osadzone, nie potrzeba `--add-data`.
Na komputerze docelowym Python nie jest wymagany. Windows EXE kompiluj na Windows,
nie na Linuxie. PyInstaller pakietuje biblioteki PDF/XLSX; plik może być duży.
Nie można zagwarantować działania na każdym komputerze bez testu docelowego systemu.
Najpierw uruchom EXE na jednym komputerze z Windows i sprawdź import/eksport.

Diagnostyka kompilacji: uruchom tę samą komendę bez `--windowed`, aby widzieć konsolę.

## Praca z programem

1. Wpisz projekt, klienta i numer/rewizję. Dodaj pliki/ZIP lub wklej tekst ze schowka.
2. Kliknij „Analizuj materiały”. Odczyt działa w wątku; komunikaty i pasek postępu
   aktualizują się bez wywoływania Tkinter z wątku roboczego.
3. W „Pełny odczyt i pliki” sprawdź wszystkie błędy, pominięcia i fragmenty OCR.
4. W rejestrze filtruj obszar lub szukaj tekstu. Dwuklik otwiera edytor.
5. Rozdziel zakres całego projektu i dostawę Zekon. Potwierdź wymagania po przeglądzie
   oryginałów; opcje nieobowiązujące oznacz „Nie obowiązuje”.
6. Sprzeczność oznacz ręcznie statusem „Do wyjaśnienia - sprzeczność”, wpisz oba
   wymagania i oba źródła w edytorze. Program nie rozstrzyga, który dokument ma pierwszeństwo.
7. „Dodaj uwagę” umożliwia zapis obserwacji z grafiki / detalu lub brakującego załącznika.
8. Zapisz sesję JSON, aby zachować potwierdzenia, korekty, BOM i tekst źródłowy.
   Wczytanie sesji nie wymaga ponownego dostępu do oryginalnych dokumentów.
9. Generuj raport: XLSX i HTML. Niepotwierdzone fragmenty pozostają w rejestrze;
   do kolumny „Wymaganie” karty trafiają tylko ustalenia ze statusem „Potwierdzone”.
10. Otwórz HTML w przeglądarce → Ctrl+P → Zapisz jako PDF. Układ do druku:
    A4 poziomo. To świadomy wybór bez dodatkowej biblioteki PDF i fontów do instalacji.

Nowa analiza zastępuje rejestr potwierdzeń po ostrzeżeniu. Zapisz sesję przed jej
uruchomieniem. Import BOM zastępuje poprzedni BOM po potwierdzeniu.

## BOM: walidacja i obliczenia

BOM importuje się osobno przez „Import BOM”, z CSV lub aktywnego arkusza XLSX.
Nagłówki mają być w pierwszym wierszu. Wymagane kolumny: `Profil`, `Ilość szt`.
Najlepiej użyć `BOM_szablon.csv` / przycisku „Szablon BOM”. Dostępne pola:

- Pozycja, Profil, Gatunek, Ilość szt, Długość, Jednostka długości (`m` / `mm`),
  kg/m, Masa kg (łączna masa danej pozycji, nie masa jednej sztuki).
- Obliczenie: ilość × długość w metrach × kg/m. Konwersja mm → m wyłącznie
  przy jawnie podanej jednostce.
- Ilość szt musi być dodatnią liczbą całkowitą, długość i kg/m dodatnie.
- Akceptowane liczby z przecinkiem lub kropką; mieszanego separatora nie zgaduje.
- Masa podana i obliczona pozostają w oddzielnych kolumnach.
- Rozbieżność przekraczająca max(0,01 kg; 0,5% masy podanej) jest sygnalizowana.
  To próg aplikacji, nie norma wykonania.
- Formuły w wejściowym XLSX są odrzucane jako dane liczbowe. W Excelu zapisz
  do importu osobną kopię tabeli jako wartości.
- Brak gatunku / ilości / jednostki / masy oznaczany w kolumnie Status.
- Program nie dodaje odpadu, kg/m z własnej bazy, gęstości stali, marży,
  pracochłonności ani ceny. Nie łączy różnych gatunków czy różnych źródeł masy.
- Tabel PDF/DOCX i geometrii IFC nie przekształca automatycznie w BOM.

Raport XLSX: Projekt, Karta wymagań, Uwagi technologiczne, Wszystkie ustalenia,
BOM, Pliki. Filtry, zawijanie tekstu, zablokowany nagłówek, ustawienia druku.

## Obsługa błędów

Uszkodzony / nieobsługiwany plik nie przerywa całej analizy. Jest w spisie plików
z przyczyną. Hasła do PDF/ZIP nie są zgadywane. Limit pojedynczego pliku: 100 MB;
łącznej partii / rozpakowanego ZIP: 500 MB; 2000 wpisów ZIP; 2000 stron PDF;
200 000 wierszy XLSX. Duże analizy podziel na partie. Archiwa nie wykonują kodu.
Tekst eksportowany do XLSX jest zabezpieczany przed wstrzyknięciem formuły.
Błędy GUI/eksportu pokazują komunikat, szczegóły zapisują do:
`%LOCALAPPDATA%\ZekonRFQ\zekon_rfq.log`.
Źródła są otwierane tylko do odczytu, bez nadpisywania.

## Weryfikacja tej wersji

Wykonano 10 testów silnika: reguły wielojęzyczne, checkboxy i brak automatycznej
akceptacji, konwersja mm, przecinek dziesiętny, brak jednostki, wejściowa formuła,
rozbieżność mas, ZIP/duplikat/nieobsługiwany plik, limit archiwum, uszkodzony PDF
obok prawidłowego pliku, zapis/odczyt sesji, eksport XLSX/HTML i formuły w tekście.
Przeprowadzono odczyt 10 załączników zapytania 151802 (PDF/DOCX/IFC): 10 plików
odczytanych, 1974 fragmenty kandydujące. Ten licznik nie potwierdza kompletności
analizy semantycznej i wizualnej. Zapis XLSX i HTML zakończył się poprawnie.
Sprawdzono składnię Python. Testy i integracja: PyMuPDF 1.26.6, openpyxl 3.1.5.
GUI i Windows EXE nie zostały uruchomione w środowisku przygotowania (Linux bez
serwera wyświetlania). Pakiet zawiera kod i skrypt budowania, nie gotowy EXE.

Uruchom testy:
```powershell
.\.venv\Scripts\python.exe -m unittest test_engine.py -v
```

## Dokumentacja zależności

- https://pyinstaller.org/en/stable/usage.html
- https://pymupdf.readthedocs.io/en/latest/page.html
- https://openpyxl.readthedocs.io/en/stable/_modules/openpyxl/reader/excel.html

Przy dystrybucji sprawdź warunki licencji zależności; PyMuPDF ma model AGPL /
licencję komercyjną. Pozostałe biblioteki i logo również mają własne warunki użycia.

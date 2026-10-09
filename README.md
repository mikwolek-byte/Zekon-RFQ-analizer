# Zekon RFQ 1.1 — jedno okno

## Obsługa
1. Uruchom Zekon_RFQ.exe.
2. Przeciągnij wszystkie pliki do białego pola. Możesz też kliknąć pole i wybrać wiele plików.
3. Kliknij **Generuj raport** i wskaż miejsce zapisu.

Program zapisuje XLSX i HTML obok siebie, a następnie otwiera HTML w przeglądarce. HTML można wydrukować do PDF. Kolejne przeciągnięcie plików po zakończeniu rozpoczyna nowe zapytanie. Przed generowaniem klawisz Delete usuwa zaznaczone pliki.

## Raport
Karta wymagań zawiera odczytane zapisy i dokładne lokalizacje źródłowe. Dodatkowe uwagi obejmują m.in. bolce NELSON, przeciwstrzałkę, gwinty, odwodnienie, stal nierdzewną, profile spawane, S275/S420/S460/S690, słupy krzyżowe, frezowanie i powierzchnie kontaktowe — PL/DE/EN/FR.
Braki oznaczane są „Do wyjaśnienia”. Zapisy automatyczne wymagają weryfikacji w oryginałach. Program nie zatwierdza sam checkboxów, negacji ani zakresu Zekon. W krótkiej karcie podaje tylko parametry i tematy, bez cytowania opisów. Powtórzenia łączy. Analizuje całą warstwę tekstową, a pełny rejestr źródeł przechowuje w ukrytym arkuszu XLSX „Wszystkie ustalenia” (Excel: Odkryj arkusz). HTML zawiera tylko raport skrócony. Projekt i klient są odczytywane tylko z jednoznacznie podpisanych pól; brak lub różne wartości pozostają do wyjaśnienia.

## Pliki i ograniczenia
PDF z tekstem, XLSX/XLSM, DOCX, TXT, CSV, IFC (wyłącznie właściwości tekstowe), ZIP. RAR, DWG, geometria IFC i OCR nie są obsługiwane; raport wskazuje pliki nieodczytane. Zagnieżdżone archiwa nie są analizowane. Maksymalnie 100 MB na plik i 500 MB danych w analizie. Odczyt nie modyfikuje plików źródłowych; materiały pozostają lokalnie.
BOM jest automatycznie importowany z osobnych CSV/XLSX z nagłówkami zgodnymi z BOM_szablon.csv. Masa = ilość × długość w metrach × kg/m. Brakujące jednostki i wartości nie są przyjmowane domyślnie. BOM z PDF/IFC/ZIP nie jest automatycznie rekonstruowany.

## Kompilacja Windows
Python 3.12 64-bit:
```bat
python -m pip install -r requirements.txt "pyinstaller>=6.16,<7"
python -m unittest -v test_engine
python -m PyInstaller --clean --noconfirm --onefile --windowed --name Zekon_RFQ --collect-all tkinterdnd2 zekon_rfq.py
```
Wynik: dist/Zekon_RFQ.exe. Można też uruchomić BUDUJ_EXE.bat. GitHub Actions buduje plik i sprawdza odczyt, BOM, inicjalizację tkdnd, obsługę przeciąganych ścieżek ze spacjami i uruchomienie gotowego EXE. Test programowy nie zastępuje ręcznego sprawdzenia przeciągania plików z Eksploratora na komputerze użytkownika.
Log błędów: %LOCALAPPDATA%/ZekonRFQ/zekon_rfq.log.

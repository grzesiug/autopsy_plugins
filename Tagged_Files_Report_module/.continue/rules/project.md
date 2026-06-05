# Tagged Files Report Module — Autopsy Plugin

## Opis projektu
Plugin dla Autopsy (narzędzie forensyczne) napisany w Pythonie/Jython.
Generuje raporty HTML o oznaczonych plikach w sprawie.

## Struktura projektu
- `TaggedFilesReportModule.py` — główny moduł pluginu
- `Language.py` — obsługa tłumaczeń/wielojęzyczności  
- `language/` — pliki językowe
- `html/` — szablony HTML raportów
- `res/` — zasoby (obrazy, CSS)
- `ffmpeg/` — narzędzie do obsługi multimediów
- `ImageMagick/` — narzędzie do obsługi obrazów

## Technologie
- Python 2/3 (Jython na JVM)
- Autopsy API (org.sleuthkit.autopsy)
- Java interop przez Jython

## Ważne klasy Autopsy API
- `org.sleuthkit.autopsy.casemodule.Case`
- `org.sleuthkit.autopsy.coreutils.Version`
- `org.sleuthkit.autopsy.coreutils.Logger`

## Zasady kodowania
- Kodowanie UTF-8
- Kompatybilność z Jython (Java + Python)
- Logi przez Java Logger
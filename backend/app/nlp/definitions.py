from dataclasses import dataclass

@dataclass(frozen=True)
class AspectDefinition:
    key: str
    keywords: list[str]

class AspectCatalog:
    ASPECTS: list[AspectDefinition] = [
        AspectDefinition("battery", ["bateria", "czas pracy", "ładowanie", "sot", "battery", "charging", "life", "mah"]),
        AspectDefinition("screen", ["ekran", "wyświetlacz", "jasność", "oled", "amoled", "hz", "screen", "display", "brightness"]),
        AspectDefinition("memory", ["pamięć", "dysk", "miejsce", "gb", "tb", "memory", "storage"]),
        AspectDefinition("ram_memory", ["ram", "pamięć operacyjna", "wielozadaniowość"]),
        AspectDefinition("camera", ["aparat", "zdjęcia", "kamera", "wideo", "zoom", "selfie", "camera", "photo", "video"]),
        AspectDefinition("performance", ["wydajność", "procesor", "zacinanie", "płynność", "gry", "cpu", "performance", "lag"]),
        AspectDefinition("design", ["wygląd", "obudowa", "kolor", "wykonanie", "design", "body", "build"]),
        AspectDefinition("quick_charge", ["szybkie ładowanie", "fast charging", "watów", "ładowarka"]),
        AspectDefinition("audio", ["głośniki", "dźwięk", "muzyka", "audio", "sound", "speakers"]),
        AspectDefinition("price", ["cena", "koszt", "opłacalność", "drogi", "tani", "price", "cost", "value"])
    ]

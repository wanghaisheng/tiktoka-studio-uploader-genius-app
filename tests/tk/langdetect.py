from eld import LanguageDetector

text="4444"
detector = LanguageDetector()

lang=detector.detect(text).language
print(lang)


text=4444
detector = LanguageDetector()

lang=detector.detect(text).language
print(lang)

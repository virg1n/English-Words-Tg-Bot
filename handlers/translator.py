from googletrans import Translator

def translate(text, src="en", dest="ru"):
    try:
        translator = Translator()
        translation = translator.translate(text=text, src=src, dest=dest)
        if (translator.detect(text).lang != translator.detect(translation.text).lang) and (text != translation.text):
            print(1, )
            return translation
        else:
            return translator.translate(text=text, src=dest, dest=src)

    except:
        return (False)

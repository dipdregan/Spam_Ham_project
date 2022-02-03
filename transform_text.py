def transform_text(text):
    text = text.lower()  # conveting all the text into a lower case
    text = nltk.word_tokenize(text)  # Tokenzation
    # this will remove special characture
    y = []
    for i in text:
        if i.isalnum():
            y.append(i)
    # this will helps to remove stopwords
    from nltk.corpus import stopwords
    import string
    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)
    text = y[:]
    y.clear()

    from nltk.stem.porter import PorterStemmer
    ps = PorterStemmer()

    for i in text:
        y.append(ps.stem(i))

    return ' '.join(y)

transform_text('djkhdfhkjksakdkf sdhksd!!Rdr>><dasdfSDF te the is are')
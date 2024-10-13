import string

BASE62 = string.ascii_letters + string.digits


def encode(num, alphabet=BASE62):
    """Encode a positive number in Base X

    Arguments:
    - `num`: The number to encode
    - `alphabet`: The alphabet to use for encoding
    """
    if num == 0:
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
        rem = num % base
        num = num // base
        arr.append(alphabet[rem])
    arr.reverse()
    return "".join(arr)


def decode(text, alphabet=BASE62):
    """Decode a Base X encoded text into the number

    Arguments:
    - `text`: The encoded text
    - `alphabet`: The alphabet to use for encoding
    """
    base = len(alphabet)
    strlen = len(text)
    num = 0

    idx = 0
    for char in text:
        power = strlen - (idx + 1)
        num += alphabet.index(char) * (base**power)
        idx += 1

    return num

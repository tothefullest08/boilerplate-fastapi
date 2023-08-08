def parse_korean_initial_sound(input_str):
    cho = [
        "ㄱ",
        "ㄲ",
        "ㄴ",
        "ㄷ",
        "ㄸ",
        "ㄹ",
        "ㅁ",
        "ㅂ",
        "ㅃ",
        "ㅅ",
        "ㅆ",
        "ㅇ",
        "ㅈ",
        "ㅉ",
        "ㅊ",
        "ㅋ",
        "ㅌ",
        "ㅍ",
        "ㅎ",
    ]
    result = ""
    for char in input_str:
        code = ord(char) - 44032
        if 0 <= code < 11172:
            result += cho[code // 588]
        else:
            result += char
    return result

from src.common.exception import InternalException, FailureType
from src.common.logger import Logger


def parse_korean_initial_sound(input_str: str) -> str:
    try:
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
    except Exception as e:
        Logger().error(f" 초성 파싱 실패. input_str: {input_str}, e: {e}")
        raise InternalException(FailureType.DATA_PROCESSING_ERROR, "초성 파싱 실패 ")

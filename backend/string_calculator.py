from typing import List, Tuple

class StringCalculator:
    def __init__(self):
        self._called_count = 0

    def get_called_count(self) -> int:
        return self._called_count

    def reset_called_count(self) -> None:
        self._called_count = 0

    def add(self, numbers: str) -> int:
        self._called_count += 1
        if numbers is None or numbers == "":
            return 0

        nums, error = self._tokenize(numbers)
        if error:
            raise ValueError(error)

        total = 0
        for n in nums:
            if n <= 1000:  # ignore > 1000
                total += n
        return total

    def _tokenize(self, s: str) -> Tuple[List[int], str]:
        delimiters = [",", "\n"]
        numbers_part = s

        if s.startswith("//"):
            header, _, rest = s.partition("\n")
            numbers_part = rest
            custom = header[2:]
            if custom.startswith("[") and custom.endswith("]"):
                delims = []
                buff = ""
                in_bracket = False
                for ch in custom:
                    if ch == "[" and not in_bracket:
                        in_bracket = True
                        buff = ""
                    elif ch == "]" and in_bracket:
                        in_bracket = False
                        delims.append(buff)
                    elif in_bracket:
                        buff += ch
                if delims:
                    delimiters = delims + ["\n"]
            else:
                if custom:
                    delimiters = [custom] + ["\n"]

        temp = numbers_part
        for d in sorted(delimiters, key=len, reverse=True):
            temp = temp.replace(d, ",")

        items = [x for x in temp.split(",") if x != ""]
        values = []
        negatives = []
        for it in items:
            # explicit decimal rejection (friendlier than generic "invalid")
            if any(ch in it for ch in ["."]):
                return [], f"decimal numbers not allowed: {it!r}"
            try:
                val = int(it)
                if val < 0:
                    negatives.append(val)
                values.append(val)
            except ValueError:
                return [], f"invalid number: {it!r}"

        if negatives:
            return [], "negatives not allowed: " + ", ".join(map(str, negatives))

        return values, ""

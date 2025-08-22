
from typing import List, Tuple

class StringCalculator:
    def __init__(self):
        self._called_count = 0

    def get_called_count(self) -> int:
        return self._called_count

    def add(self, numbers: str) -> int:
        self._called_count += 1
        if numbers is None or numbers == "":
            return 0

        nums, error = self._tokenize(numbers)
        if error:
            raise ValueError(error)

        total = 0
        for n in nums:
            if n <= 1000:  # Rule 9: ignore > 1000
                total += n
        return total

    def _tokenize(self, s: str) -> Tuple[List[int], str]:
        # Rules 3-4, 10-12: delimiter parsing
        delimiters = [",", "\n"]
        numbers_part = s
        if s.startswith("//"):
            header, _, rest = s.partition("\n")
            numbers_part = rest
            custom = header[2:]  # after //
            if custom.startswith("[") and custom.endswith("]"):
                # multiple or long delimiters: //[delim][delim2]...
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
                # single char delimiter like //;\n
                if custom:
                    delimiters = [custom] + ["\n"]

        # Build a unified split using replacement
        temp = numbers_part
        for d in sorted(delimiters, key=len, reverse=True):
            # escape special regex characters by simple replace usage later
            temp = temp.replace(d, ",")
        # Validate invalid patterns like "1,\n" not required by kata (we keep it simple)

        # Convert to integers, collect negatives for error
        items = [x for x in temp.split(",") if x != ""]
        values = []
        negatives = []
        for it in items:
            try:
                val = int(it)
                if val < 0:
                    negatives.append(val)
                values.append(val)
            except ValueError:
                return [], f"invalid number: {it!r}"

        if negatives:
            # Rules 5-6: negatives not allowed, show all
            return [], "negatives not allowed: " + ", ".join(map(str, negatives))

        return values, ""

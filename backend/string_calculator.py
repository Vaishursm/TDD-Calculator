import re
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
                # multiple or long delimiters: //[delim1][delim2]...
                delimiters = re.findall(r"\[(.*?)\]", custom)
            else:
                delimiters = [custom]

        # Escape regex special chars for each delimiter
        escaped_delims = [re.escape(d) for d in delimiters]
        pattern = "|".join(escaped_delims)

        # Split numbers using regex
        items = [x for x in re.split(pattern, numbers_part) if x != ""]

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
            return [], "negatives not allowed: " + ", ".join(map(str, negatives))

        return values, ""

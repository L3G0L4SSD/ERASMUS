def brute_force_with_wildcards(text, pattern):
    def matches_at(text, pattern, text_index, pattern_index):
        while pattern_index < len(pattern):
            if pattern[pattern_index] == '\\':
                pattern_index += 1
                if pattern_index >= len(pattern) or text_index >= len(text) or pattern[pattern_index] != text[text_index]:
                    return False
            elif pattern[pattern_index] == '?':
                if text_index >= len(text):
                    return False
            elif pattern[pattern_index] == '*':
                while pattern_index < len(pattern) and pattern[pattern_index] == '*':
                    pattern_index += 1
                if pattern_index == len(pattern):
                    return True
                while text_index < len(text):
                    if matches_at(text, pattern, text_index, pattern_index):
                        return True
                    text_index += 1
                return False
            elif text_index >= len(text) or pattern[pattern_index] != text[text_index]:
                return False
            text_index += 1
            pattern_index += 1
        return pattern_index == len(pattern)

    for i in range(len(text) - len(pattern) + 1):
        if matches_at(text, pattern, i, 0):
            return True
    return False

def sunday_with_wildcards(pattern, text):
    pattern_bits = pattern.split('*')
    i = 0
    while i < len(pattern_bits) - 1:
        if pattern_bits[i].endswith('\\'):
            pattern_bits[i] = pattern_bits[i][:-1] + '*'
            pattern_bits[i] += pattern_bits[i + 1]
            del pattern_bits[i + 1]
        else:
            i += 1

    pattern_bits_truth = []
    m = len(pattern)
    n = len(text)
    i = 0

    for pbl in range(len(pattern_bits)):
        pattern_bit_match = False
        pattern_bit = pattern_bits[pbl]
        pbl_len = len(pattern_bit)
        skip_table = {}

        qqq = -1
        for j in range(pbl_len):
            if pattern_bit[j] == '?':
                qqq = j; 
        for j in range(pbl_len):
            skip_table[pattern_bit[j]] = pbl_len - max(j,qqq)
        

        while i <= n - pbl_len:
            j = 0
            while j < pbl_len and (text[i + j] == pattern_bit[j] or pattern_bit[j] == "?"):
                j += 1
            if j == pbl_len:
                pattern_bit_match = True
                break
            if i + pbl_len >= n:
                break
            skip = skip_table.get(text[i + pbl_len])
            if skip is not None:
                i += skip
            else:
                i += pbl_len + max(1,qqq)

        pattern_bits_truth.append(pattern_bit_match)
        if not pattern_bit_match:
            break

    if False in pattern_bits_truth:
        return False
    else:
        return True
text = "sbaazczzzzzzzzzzzzzzzz0"
patterns = ["a?z","ab*cbaa","a?c", "a*c", "a*c*", "\\*abc", "ab\\*c"]

print("Brute-force with wildcards:")
for pattern in patterns:
    print(f"Pattern '{pattern}' found:", brute_force_with_wildcards(text, pattern))

print("\nSunday with wildcards:")
for pattern in patterns:
    print(f"Pattern '{pattern}' found:", sunday_with_wildcards(pattern, text))
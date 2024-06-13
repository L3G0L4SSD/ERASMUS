import time
import matplotlib.pyplot as plt

with open('book.txt', 'r', encoding='utf-8') as file:
    book_content = file.read()


small_patterns = ["I saw people", "The bat smashed into ", "My teacher","The following months were "]

large_pattern = book_content.split('\n\n')[0] 


text_lengths = [1000, 5000, 10000, 50000, 100000]

while len(book_content) < max(text_lengths):
    book_content += book_content  

def brute_force(text, pattern):
    occurrences = []
    n, m = len(text), len(pattern)
    for i in range(n - m + 1):
        if text[i:i + m] == pattern:
            occurrences.append(i)
    return occurrences

def sunday(text, pattern):
    def get_shift_table(pattern):
        shift = {}
        m = len(pattern)
        for i in range(m):
            shift[pattern[i]] = m - i
        return shift

    n, m = len(text), len(pattern)
    if m > n:
        return []

    shift = get_shift_table(pattern)
    occurrences = []
    i = 0
    while i <= n - m:
        if text[i:i + m] == pattern:
            occurrences.append(i)
        if i + m >= n:
            break
        i += shift.get(text[i + m], m + 1)
    return occurrences

def kmp(text, pattern):
    def compute_lps(pattern):
        lps = [0] * len(pattern)
        length = 0
        i = 1
        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps

    n, m = len(text), len(pattern)
    lps = compute_lps(pattern)
    occurrences = []

    i = j = 0
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == m:
            occurrences.append(i - j)
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return occurrences

def fsm(text, pattern):
    def compute_fsm(pattern):
        m = len(pattern)
        alphabet = set(pattern)
        fsm = [{} for _ in range(m + 1)]
        for q in range(m + 1):
            for char in alphabet:
                k = min(m, q + 1)
                while k > 0 and pattern[:k] != (pattern[:q] + char)[-k:]:
                    k -= 1
                fsm[q][char] = k
        return fsm

    m = len(pattern)
    fsm = compute_fsm(pattern)
    state = 0
    occurrences = []
    for i, char in enumerate(text):
        if char in fsm[state]:
            state = fsm[state][char]
        else:
            state = 0
        if state == m:
            occurrences.append(i - m + 1)
    return occurrences

def rabin_karp(text, pattern, q=101):
    d = 256
    n, m = len(text), len(pattern)
    h = pow(d, m-1) % q
    p = 0
    t = 0
    occurrences = []

    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    for i in range(n - m + 1):
        if p == t:
            if text[i:i + m] == pattern:
                occurrences.append(i)
        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q
            if t < 0:   
                t += q
    return occurrences

def gusfield_z(text, pattern):
    def compute_z(s):
        z = [0] * len(s)
        l, r, k = 0, 0, 0
        for i in range(1, len(s)):
            if i > r:
                l, r = i, i
                while r < len(s) and s[r] == s[r - l]:
                    r += 1
                z[i] = r - l
                r -= 1
            else:
                k = i - l
                if z[k] < r - i + 1:
                    z[i] = z[k]
                else:
                    l = i
                    while r < len(s) and s[r] == s[r - l]:
                        r += 1
                    z[i] = r - l
                    r -= 1
        return z

    combined = pattern + '$' + text
    z = compute_z(combined)
    occurrences = [i - len(pattern) - 1 for i in range(len(pattern) + 1, len(z)) if z[i] == len(pattern)]
    return occurrences

def measure_time(func, text, pattern):
    start = time.time() * 10000
    n = 10
    for _ in range(n):
        func(text, pattern)
    end = time.time() * 10000
    return (end - start)/n 

results_small = {
    "Brute-force": [],
    "Sunday": [],
    "KMP": [],
    "FSM": [],
    "Rabin-Karp": [],
    "Gusfield Z": []
}

results_large = {
    "Brute-force": [],
    "Sunday": [],
    "KMP": [],
    "FSM": [],
    "Rabin-Karp": [],
    "Gusfield Z": []
}

for pattern in small_patterns:
    print(f"Testing small pattern: '{pattern}'")
    for length in text_lengths:
        truncated_text = book_content[:length]
        results_small["Brute-force"].append(measure_time(brute_force, truncated_text, pattern))
        results_small["Sunday"].append(measure_time(sunday, truncated_text, pattern))
        results_small["KMP"].append(measure_time(kmp, truncated_text, pattern))
        results_small["FSM"].append(measure_time(fsm, truncated_text, pattern))
        results_small["Rabin-Karp"].append(measure_time(rabin_karp, truncated_text, pattern))
        results_small["Gusfield Z"].append(measure_time(gusfield_z, truncated_text, pattern))

print(f"Testing large pattern (paragraph)")

for length in text_lengths:
    truncated_text = book_content[:length]
    results_large["Brute-force"].append(measure_time(brute_force, truncated_text, large_pattern))
    results_large["Sunday"].append(measure_time(sunday, truncated_text, large_pattern))
    results_large["KMP"].append(measure_time(kmp, truncated_text, large_pattern))
    results_large["FSM"].append(measure_time(fsm, truncated_text, large_pattern))
    results_large["Rabin-Karp"].append(measure_time(rabin_karp, truncated_text, large_pattern))
    results_large["Gusfield Z"].append(measure_time(gusfield_z, truncated_text, large_pattern))


print("Running times for small patterns:")
for algorithm, times in results_small.items():
    print(f"{algorithm}: {times}")

print("Running times for large pattern:")
for algorithm, times in results_large.items():
    print(f"{algorithm}: {times}")


plt.figure(figsize=(12, 8))

for algorithm in results_small:
    plt.plot(text_lengths, results_small[algorithm][:len(text_lengths)], label=f"{algorithm}")

plt.xlabel('Text Length')
plt.ylabel('Running Time (milliseconds)')
plt.title('Pattern Matching Algorithms Running Time Comparison (Small Patterns)')
plt.legend()
plt.show()


plt.figure(figsize=(12, 8))

for algorithm in results_large:
    plt.plot(text_lengths, results_large[algorithm], label=f"{algorithm}")

plt.xlabel('Text Length')
plt.ylabel('Running Time (milliseconds)')
plt.title('Pattern Matching Algorithms Running Time Comparison (Large Pattern)')
plt.legend()
plt.show()


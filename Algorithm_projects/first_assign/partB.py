import time
import random
import string
import matplotlib.pyplot as plt

text = ("01" * 50000)[:100000]  
pattern1 = "07070707jsjbscbbshbcbscbs"
pattern2 = ("01" * 50000)[:100000]  




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

# Function to measure running time
def measure_time(func, text, pattern):
    start = time.time()
    func(text, pattern)
    end = time.time()
    return (end - start) * 1000  # Convert to milliseconds

# Empirical tests

# Binary Sunday vs. Gusfield Z
time_binary_sunday = measure_time(sunday, text, pattern1)
time_gusfield_z = measure_time(gusfield_z, text, pattern1)

# KMP vs. Rabin-Karp
time_kmp = measure_time(kmp, text, pattern1)
time_rabin_karp = measure_time(rabin_karp, text, pattern1)

# Rabin-Karp vs. Sunday
time_rabin_karp_rare = measure_time(rabin_karp, text, pattern2)
time_sunday = measure_time(sunday, text, pattern2)

# Result2
print(f"Binary Sunday vs. Gusfield Z")
print(f"Binary Sunday: {time_binary_sunday:.2f} ms")
print(f"Gusfield Z: {time_gusfield_z:.2f} ms")
# print(f"Ratio: {time_gusfield_z / time_binary_sunday:.2f}")

print(f"\nKMP vs. Rabin-Karp")
print(f"KMP: {time_kmp:.2f} ms")
print(f"Rabin-Karp: {time_rabin_karp:.2f} ms")
# print(f"Ratio: {time_rabin_karp / time_kmp:.2f}")

print(f"\nRabin-Karp vs. Sunday")
print(f"Rabin-Karp: {time_rabin_karp_rare:.2f} ms")
print(f"Sunday: {time_sunday:.2f} ms")
# print(f"Ratio: {time_sunday / time_rabin_karp_rare:.2f}")


# Plotting the results
labels = ['Binary Sunday', 'Gusfield Z', 'KMP', 'Rabin-Karp', 'Rabin-Karp -', 'Sunday']
times = [time_binary_sunday, time_gusfield_z, time_kmp, time_rabin_karp, time_rabin_karp_rare, time_sunday]

plt.figure(figsize=(10, 6))
plt.bar(labels, times, color=['blue', 'orange', 'green', 'red', 'purple', 'brown'])
plt.xlabel('Algorithm')
plt.ylabel('Time (ms)')
plt.title('Performance Comparison of Pattern Matching Algorithms')
plt.show()
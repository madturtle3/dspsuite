import numpy as np

LETTERS = [
    "\b",
    "E",
    "\n",
    "A",
    " ",
    "S",
    "I",
    "U",
    "\r",
    "D",
    "R",
    "J",
    "N",
    "F",
    "C",
    "K",
    "T",
    "Z",
    "L",
    "W",
    "H",
    "Y",
    "P",
    "Q",
    "O",
    "B",
    "G",
    "FIGURES",
    "M",
    "X",
    "V",
    "LETTERS",
]
FIGURES = [
    "\b",
    "3",
    "\n",
    "-",
    " ",
    "8",
    "7",
    "\r",
    "$",
    "4",
    "'",
    ",",
    "!",
    ":",
    "(",
    "5",
    '"',
    ")",
    "2",
    "=",
    "6",
    "0",
    "1",
    "9",
    "?",
    "+",
    "FIGURES",
    ".",
    "/",
    ";",
    "LETTERS",
]

RATE = 44100
BAUD = 45
SPB = int(RATE/BAUD)
msg = "HELLO THERE!"
numbers = []
mode = "LETTERS"
for ch in msg.upper():
    if ch in LETTERS:
        if mode == "FIGURES":
            mode = "LETTERS"
            numbers.append(FIGURES.index("LETTERS"))
        numbers.append(LETTERS.index(ch))
    elif ch in FIGURES:
        if mode == "LETTERS":
            mode = "FIGURES"
            numbers.append(LETTERS.index("FIGURES"))
        numbers.append(FIGURES.index(ch))
    else:
        print("invalid character",ch)
binary: list[str] = []
for num in numbers:
    binstr = bin(num)[2:]
    binstr = "0"*(5-len(binstr)) + binstr
    # least significant bit
    binstr = binstr[::-1]
    binary.append(binstr)
zero = np.repeat([1800*2*np.pi/RATE],SPB)
one = np.repeat([1400*2*np.pi/RATE],SPB)
# modulate
samples = np.zeros(SPB*5)
for baudot in binary:
    baudot = baudot
    samples = np.concatenate((samples,zero))
    for bit in baudot:
        samples = np.concatenate((samples,zero if bit=="0" else one))
    samples = np.concatenate((samples,one,one))
samples = np.cos(np.cumsum(samples))
samples = np.concatenate((samples,np.zeros(SPB*5)))
import scipy.io.wavfile as wavfile
wavfile.write("test.wav",RATE,samples)
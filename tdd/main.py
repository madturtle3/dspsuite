import numpy as np
import numpy.typing as npt
import scipy.signal as signal
import scipy.io.wavfile as wave
import matplotlib.pyplot as plt

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
    "",
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

BAUD = 45


def main():
    rate, samples = wave.read("test.wav")
    SPB = int(rate / BAUD)
    filt = signal.firls(
        175,
        [0, 1300, 1400, 1800, 1900, rate / 2],
        desired=[0, 0, 1, 1, 0, 0],
        fs=rate,
    )
    samples = signal.lfilter(filt, 1, samples)
    samples = signal.hilbert(samples)
    sig1 = samples[1:]
    sig2 = np.conjugate(samples[:-1])
    prod = sig1 * sig2
    anglediff = np.angle(prod)
    freq = anglediff / (2 * np.pi) * rate
    binout = (np.abs(freq - 1400) < np.abs(freq - 1800)).astype(np.int16)
    baudot_template = np.concat(
        (np.repeat(-1, SPB), np.repeat(0, SPB * 5), np.repeat(1, SPB * 2))
    )
    baud_detect = np.correlate(2 * binout - 1, baudot_template)
    maxmima,properties = signal.find_peaks(baud_detect,2750,plateau_size=(None,None))
    peaks_unrefined = properties["left_edges"]
    peaks = [peaks_unrefined[0]]
    diffs = np.diff(peaks_unrefined)
    for i in range(1,peaks_unrefined.shape[0]):
        if diffs[i-1]>SPB*5:
            peaks.append(peaks_unrefined[i])

    mode = "LETTERS"
    plt.plot(freq)
    plt.plot(baud_detect)
    plt.plot(peaks_unrefined,baud_detect[peaks_unrefined],"x")
    plt.plot(peaks,baud_detect[peaks],"x")
    
    plt.show()
    for i in peaks:
        idxs = [int(i + (1.5 + k) * SPB) for k in range(5)]
        val = 0
        for j,digit in enumerate(binout[idxs]):
            val |= digit<<j
            #print(val)
        if FIGURES[val] == "LETTERS":
            mode = "LETTERS"
        elif LETTERS[val] == "FIGURES":
            mode = "FIGURES"
        else:
            if mode == "LETTERS":
                print(LETTERS[val],end="",flush=True)
            elif mode == "FIGURES":
                print(FIGURES[val],end="",flush=True)
    print()

if __name__ == "__main__":
    main()

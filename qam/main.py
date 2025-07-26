# in comes the PSK!
import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt


def getbits(bytearr: bytes, bytesize: int = 8) -> list[int]:
    bits: list[int] = []
    for byte in bytearr:
        bits += [(byte >> i) & 1 for i in range(bytesize)]
    return bits


def getbytes(bits: list[int], bytesize: int = 8) -> bytes:
    bytelist: list[int] = []
    for i in range(0, len(bits), bytesize):
        cur_byte: int = 0
        for j in range(bytesize):
            cur_byte |= bits[i + j] << j
        bytelist.append(cur_byte)
    return bytes(bytelist)


def modulate(
    coded: npt.NDArray[np.complexfloating],
    Fs: int = 8000,
    Fb: float = 50,
    Fc: float = 700,
) -> npt.NDArray[np.floating]:
    """
    Quite literally just turns complex numbers into a signal.
    """
    Spb: int = int(Fs / Fb)
    IQ = np.repeat(coded, Spb)
    # later on you may optionally convolve this to smooth out your baud boundaries
    # be more spectrally efficient
    time = np.arange(0, IQ.shape[0]) * 2 * np.pi * Fc / Fs
    samples = IQ.real * np.cos(time) / 2 + IQ.imag * np.sin(time) / 2
    return samples


if __name__ == "__main__":
    # how on earth do I code bytes into something interesting????
    samples = modulate(np.array([1 + 3j, 2 + 1j]))
    plt.plot(samples)
    plt.show()

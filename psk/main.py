# in comes the PSK!
import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt


def getbits(bytearr: bytes) -> list[int]:
    """
    Turns bytes into a list of ones and zeros.
    """
    bits: list[int] = []
    for byte in bytearr:
        bits += [(byte >> i) & 1 for i in range(8)]
    return bits


def getbytes(bits: list[int], bytesize: int = 8) -> bytes:
    """
    Turns a list of ones and zeros into numbers
    whose width is determined by bytesize.
    """
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
    # later on I may optionally convolve this to smooth out the baud boundaries
    # be more spectrally efficient
    time = np.arange(0, IQ.shape[0]) * 2 * np.pi * Fc / Fs
    # now do I*cos(x)+Q*sin(x)
    samples = IQ.real * np.cos(time) / 2 + IQ.imag * np.sin(time) / 2
    return samples


if __name__ == "__main__":
    # okay so imagine we have a message
    msg = bytes(range(256))
    # now we turn that into a bit array
    bitwidth = 1
    bits = list(getbytes(getbits(msg), bitwidth))
    print(len(bits))
    # now each element in bits is either 0,1,2, or 3.
    # now we map each one to this bit space.
    bitspace = np.linspace(-1, 1, 2**bitwidth)
    comp_in = [ bitspace[bits[x]] + 1j*bitspace[bits[x+1]] for x in range(0,len(bits),2)]

    # how on earth do I code bytes into something interesting????
    samples = modulate(np.array(comp_in), Fc=100)
    plt.plot(samples)
    plt.show()

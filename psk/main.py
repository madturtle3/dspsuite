# in comes the PSK!
import numpy as np
import numpy.typing as npt
import scipy.signal as signal
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
    msg: npt.NDArray[np.complexfloating],
    Fs: int = 8000,
    Fb: float = 50,
    Fc: float = 700,
) -> npt.NDArray[np.floating]:
    """
    Quite literally just turns complex numbers into a signal.
    """
    Spb: int = int(Fs / Fb)
    IQ = np.repeat(msg, Spb)
    # smooth it for less splatter
    smooth = np.ones(10)
    IQ = np.convolve(IQ,smooth,"same")
    IQ = np.convolve(IQ,smooth,"same")
    IQ = np.convolve(IQ,smooth,"same")
    IQ = np.convolve(IQ,smooth,"same")
    # later on I may optionally convolve this to smooth out the baud boundaries
    # be more spectrally efficient
    time = np.arange(0, IQ.shape[0]) * 2 * np.pi * Fc / Fs
    # now do I*cos(x)+Q*sin(x)
    samples = IQ.real * np.cos(time) / 2 + IQ.imag * np.sin(time) / 2
    plt.plot(samples)
    plt.show()
    return samples


def demodulate(
    samples: npt.NDArray[np.floating], Fs: int = 8000, Fc: float = 700
) -> npt.NDArray[np.complexfloating]:
    taps = signal.firls(81,[[0,Fc-50],[Fc-50,Fc+50],[Fc+50,Fs//2]],[[0,0],[1,1],[0,0]],fs=Fs)
    filtered: npt.NDArray[np.floating] = np.convolve(samples,taps,"same")
    time: npt.NDArray[np.floating] = (
        np.arange(samples.shape[0], dtype=np.float32) * 2 * np.pi * Fc / Fs
    )
    iq: npt.NDArray[np.complexfloating] = np.cos(time) + 1j * np.sin(time)
    iq *= filtered * 2
    smoother = np.ones(int(Fs/Fc)) / int(Fs/Fc)
    compout = np.convolve(iq,smoother,"same")
    return compout

if __name__ == "__main__":
    comp_in: list[complex] = [1,1,1,-1,1,1]
    # how on earth do I code bytes into something interesting????
    samples = modulate(np.array(comp_in))
    demod = demodulate(samples)
    plt.plot(samples)
    plt.plot(demod.real)
    plt.plot(demod.imag)
    plt.show()

import sys
import optparse
import numpy as np

K = 2


def encode(stream):
    """Encode the stream."""
    block = []
    arr = np.zeros((K + 1, K + 1), dtype=np.uint8)
    while 1:
        num = stream.read(1)
        if num in ['\n', '']:
            break
        num = int(num)
        block.append(num)
        if len(block) == K * K:
            # apply algoritm
            arr[:K, :K] = np.reshape(block, (K, K))
            arr[0:K, K] = np.bitwise_xor.reduce(arr[:K, :K], axis=1)
            arr[K, 0:K] = np.bitwise_xor.reduce(arr[:K, :K], axis=0)
            for out in arr.ravel()[:-1]:
                yield str(out)  # skip last char
            block = []


def decode(stream):
    """Decode the stream"""
    block = []
    while 1:
        num = stream.read(1)
        if num in ['\n', '']:
            break
        num = int(num)
        block.append(num)
        N = K * (K + 2)
        if len(block) == N:
            arr = np.resize(block, N + 1).reshape((K + 1, K + 1))
            # XOR columns
            col_xors = np.bitwise_xor.reduce(arr[:K, :K + 1], axis=1)
            nonzero_cols = col_xors.nonzero()[0]
            # XOR rows
            row_xors = np.bitwise_xor.reduce(arr[:K + 1, :K], axis=0)
            nonzero_rows = row_xors.nonzero()[0]
            if nonzero_cols.shape == nonzero_rows.shape == (0,):
                # no errors or undetected errors
                pass
            elif nonzero_cols.shape == (0,) and nonzero_rows.shape == (1,):
                # assuming parity bit error
                pass
            elif nonzero_rows.shape == (0,) and nonzero_cols.shape == (1,):
                # assuming parity bit error
                pass
            elif nonzero_cols.shape == nonzero_rows.shape == (1,):
                row = nonzero_cols[0]
                col = nonzero_rows[0]
                # flip that bit
                arr[row, col] = 1 - arr[row, col]
            else:
                # more than 1 errors
                print(nonzero_cols)
                print(nonzero_rows)
                raise Exception('Cannot detect error.')

            for out in np.ravel(arr[:K, :K]):
                yield str(out)  # skip last char

            block = []


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-e', '--encode', action='store_true', dest='encode', default=True,
                      help='Encode the input stream.')
    parser.add_option('-d', '--decode', action='store_true', dest='decode', default=False,
                      help='Decode the input stream.')
    opts = parser.parse_args()[0]
    func = decode if opts.decode else encode

    for enc in func(sys.stdin):
        sys.stdout.write(enc)

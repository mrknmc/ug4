import sys
import optparse
import numpy as np


def encode(stream):
    """Encode the stream."""
    block = []
    arr = np.zeros((5, 5), dtype=np.uint8)
    while 1:
        num = stream.read(1)
        if num in ['\n', '']:
            break
        num = int(num)
        block.append(num)
        if len(block) == 16:
            # apply algoritm
            arr[:4, :4] = np.reshape(block, (4, 4))
            arr[0:4, 4] = np.bitwise_xor.reduce(arr[:4, :4], axis=1)
            arr[4, 0:4] = np.bitwise_xor.reduce(arr[:4, :4], axis=0)
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
        if len(block) == 24:
            arr = np.resize(block, 25).reshape((5, 5))
            # XOR columns
            col_xors = np.bitwise_xor.reduce(arr[:4, :5], axis=1)
            nonzero_cols = col_xors.nonzero()[0]
            # XOR rows
            row_xors = np.bitwise_xor.reduce(arr[:5, :4], axis=0)
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

            for out in np.ravel(arr[:4, :4]):
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

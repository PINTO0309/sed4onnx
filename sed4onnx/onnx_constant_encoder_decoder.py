#! /usr/bin/env python

import sys
import ast
import re
import base64
import numpy as np
from argparse import ArgumentParser

class Color:
    BLACK          = '\033[30m'
    RED            = '\033[31m'
    GREEN          = '\033[32m'
    YELLOW         = '\033[33m'
    BLUE           = '\033[34m'
    MAGENTA        = '\033[35m'
    CYAN           = '\033[36m'
    WHITE          = '\033[37m'
    COLOR_DEFAULT  = '\033[39m'
    BOLD           = '\033[1m'
    UNDERLINE      = '\033[4m'
    INVISIBLE      = '\033[08m'
    REVERCE        = '\033[07m'
    BG_BLACK       = '\033[40m'
    BG_RED         = '\033[41m'
    BG_GREEN       = '\033[42m'
    BG_YELLOW      = '\033[43m'
    BG_BLUE        = '\033[44m'
    BG_MAGENTA     = '\033[45m'
    BG_CYAN        = '\033[46m'
    BG_WHITE       = '\033[47m'
    BG_DEFAULT     = '\033[49m'
    RESET          = '\033[0m'

DTYPES_TO_NUMPY_DTYPES: dict = {
    'float32': np.float32,
    'float64': np.float64,
    'uint8': np.uint8,
    'int8': np.int8,
    'int32': np.int32,
    'int64': np.int64,
}


def encode(
    constant_string: str,
) -> str:
    """encode

    Parameters
    ----------
    constant_string: str
        ASCII string to be encoded.

    Returns
    -------
    encoded_string: str
        Base64-encoded ASCII string.
    """

    # Return
    return base64.b64encode(np.asarray(ast.literal_eval(constant_string)).tobytes()).decode('utf-8')


def decode(
    constant_string: str,
    dtype: str,
) -> np.ndarray:
    """decode

    Parameters
    ----------
    constant_string: str
        Base64 string to be decoded.

    dtype: str
        'float32' or 'float64' or 'uint8' or 'int8' or 'int32' or 'int64'

    Returns
    -------
    decoded_ndarray: np.ndarray
        Base64-decoded numpy.ndarray.
    """

    # dtype check
    if not dtype in DTYPES_TO_NUMPY_DTYPES:
        print(
            f'{Color.RED}ERROR:{Color.RESET} '+
            f'dtype must be one of {DTYPES_TO_NUMPY_DTYPES.keys()}.'
        )
        sys.exit(1)

    # Return
    return np.frombuffer(base64.b64decode(constant_string), dtype=DTYPES_TO_NUMPY_DTYPES[dtype])


def main():
    parser = ArgumentParser()
    parser.add_argument(
        '--constant_string',
        type=str,
        required=True,
        help='Strings to be encoded and decoded for ONNX constants.'
    )
    parser.add_argument(
        '--dtype',
        type=str,
        choices=DTYPES_TO_NUMPY_DTYPES,
        help='Data type.'
    )
    parser.add_argument(
        '--mode',
        type=str,
        choices=[
            'encode',
            'decode',
        ],
        help=\
            'encode: Converts the string specified in constant_string to a Base64 format string '+
            'that can be embedded in ONNX constants. \n'+
            'decode: Converts a Base64 string specified in constant_string to ASCII like Numpy string.'
    )
    args = parser.parse_args()

    constant_string = args.constant_string
    dtype = args.dtype
    mode = args.mode

    if mode == 'encode':
        enc_dec_string = encode(
            constant_string=constant_string,
        )
        print(enc_dec_string)

    elif mode == 'decode':
        if not dtype:
            print(
                f'{Color.RED}ERROR:{Color.RESET} '+
                f'dtype must be one of {DTYPES_TO_NUMPY_DTYPES.keys()}.'
            )
            sys.exit(1)
        decoded_ndarray = decode(
            constant_string=constant_string,
            dtype=dtype,
        )
        decoded_ndarray_str = re.sub(
            pattern=r'\s+',
            repl='',
            string=np.array2string(
                decoded_ndarray,
                threshold=np.inf,
                max_line_width=np.inf,
                separator=','
            )
        )
        print(decoded_ndarray_str)


if __name__ == '__main__':
    main()


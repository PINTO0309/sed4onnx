# sed4onnx
Simple ONNX constant encoder/decoder.

https://github.com/PINTO0309/simple-onnx-processing-tools

[![Downloads](https://static.pepy.tech/personalized-badge/sed4onnx?period=total&units=none&left_color=grey&right_color=brightgreen&left_text=Downloads)](https://pepy.tech/project/sed4onnx) ![GitHub](https://img.shields.io/github/license/PINTO0309/sed4onnx?color=2BAF2B) [![PyPI](https://img.shields.io/pypi/v/sed4onnx?color=2BAF2B)](https://pypi.org/project/sed4onnx/) [![CodeQL](https://github.com/PINTO0309/sed4onnx/workflows/CodeQL/badge.svg)](https://github.com/PINTO0309/sed4onnx/actions?query=workflow%3ACodeQL)

## Key concept
- Since the constant values in the JSON files generated by **[onnx2json](https://github.com/PINTO0309/onnx2json)** are Base64-encoded values, ASCII <-> Base64 conversion is required when rewriting JSON constant values.
- After writing the converted Base64 strings to JSON using this tool, **[json2onnx](https://github.com/PINTO0309/json2onnx)** can be used to regenerate the constant-modified ONNX file.

## 1. Setup
### 1-1. HostPC
```bash
### option
$ echo export PATH="~/.local/bin:$PATH" >> ~/.bashrc \
&& source ~/.bashrc

### run
$ pip install -U sed4onnx
```
### 1-2. Docker
https://github.com/PINTO0309/simple-onnx-processing-tools#docker


## 2. CLI Usage
```bash
$ sed4onnx -h

usage:
    sed4onnx [-h]
    --constant_string CONSTANT_STRING
    [--dtype {float32,float64,uint8,int8,int32,int64}]
    [--mode {encode,decode}]

optional arguments:
  -h, --help
        show this help message and exit.

  --constant_string CONSTANT_STRING
        Strings to be encoded and decoded for ONNX constants.

  --dtype {float32,float64,uint8,int8,int32,int64}
        Data type.

  --mode {encode,decode}
        encode: Converts the string specified in constant_string to a Base64 format string
                that can be embedded in ONNX constants.
        decode: Converts a Base64 string specified in constant_string to ASCII like Numpy string.
```

## 3. In-script Usage
```python
>>> from sed4onnx import encode
>>> from sed4onnx import decode
>>> help(encode)

Help on function encode in module sed4onnx.onnx_constant_encoder_decoder:

encode(constant_string: str) -> str

    Parameters
    ----------
    constant_string: str
        ASCII string to be encoded.

    Returns
    -------
    encoded_string: str
        Base64-encoded ASCII string.


>>> help(decode)
Help on function decode in module sed4onnx.onnx_constant_encoder_decoder:

decode(constant_string: str, dtype: str) -> numpy.ndarray
    decode

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
```

## 4. CLI Execution
```bash
$ sed4onnx \
--constant_string [-1,3,224,224] \
--mode encode

$ sed4onnx \
--constant_string '//////////8DAAAAAAAAAOAAAAAAAAAA4AAAAAAAAAA=' \
--dtype int64 \
--mode decode
```

## 5. In-script Execution
```python
from sed4onnx import encode
from sed4onnx import decode

base64_string = encode(
  constant_string='[-1,3,224,224]',
)

numpy_ndarray = decode(
  constant_string='//////////8DAAAAAAAAAOAAAAAAAAAA4AAAAAAAAAA=',
  dtype='int64',
)
```

## 6. Sample
```bash
$ sed4onnx \
--constant_string [-1,3,224,224] \
--mode encode

//////////8DAAAAAAAAAOAAAAAAAAAA4AAAAAAAAAA=


$ sed4onnx \
--constant_string '//////////8DAAAAAAAAAOAAAAAAAAAA4AAAAAAAAAA=' \
--dtype int64 \
--mode decode

[-1,3,224,224]
```

## 7. Reference
1. https://github.com/onnx/onnx/blob/main/docs/Operators.md
2. https://docs.nvidia.com/deeplearning/tensorrt/onnx-graphsurgeon/docs/index.html
3. https://github.com/NVIDIA/TensorRT/tree/main/tools/onnx-graphsurgeon
4. https://github.com/PINTO0309/simple-onnx-processing-tools
5. https://github.com/PINTO0309/PINTO_model_zoo

## 8. Issues
https://github.com/PINTO0309/simple-onnx-processing-tools/issues
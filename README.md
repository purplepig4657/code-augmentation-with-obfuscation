## Code augmentation with obfuscation
- Tigress tool used for obfuscation
- Renaming of variables, functions are implemented manually.

## Prerequisites

- Tigress
- Clang (or gcc)

## Usage

```bash
mkdir data
mkdir obfuscated
python3 main.py
```

## Note

- `data` directory is used to store the source code to be obfuscated. This directory is specified in `FileLoader` and it can be changed by modifying `data_directory` while initializing `FileLoader`.
- `obfuscated` directory is used to store the obfuscated source code. This directory is specified in `Obfuscator` and it can be changed by modifying `result_path` while initializing `Obfuscator`.

## Caution
- `preprocessor.py` is not working on every platform and machines. Currently, it is confirmed to work on `Darwin-arm64` and `Linux-x86_64`.
- `rename.py` can make errors because the preprocessor isn't cover all platforms and machines.

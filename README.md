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

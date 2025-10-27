# RIPcaster CPU Emulator

## Usage
To use **RIPcaster**:
- Move your assembly code to the *RIPcaster's* directory.
- Open **config.toml** and write your assembly file's name in the `asmfile=" "` field.
  - For example, if your assembly file is *asmfile.asm*, you can write `asmfile="asmfile.asm"`.
- You can set the **RAM size** of the emulator according to your needs by writing the RAM size in the `ram_size=` field.
  - For example, to set the RAM size to 2048 bytes, write `ram_size=2048`.
- To give *RIPcaster* execution permission, run `chmod +x RIPcaster.py` in the terminal.
- To run *RIPcaster*, use `./RIPcaster.py`.
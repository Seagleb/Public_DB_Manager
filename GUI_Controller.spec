# -*- mode: python -*-

block_cipher = None


a = Analysis(['GUI_Controller.py'],
             pathex=['C:\\Users\\seagle\\Desktop\\Repositories\\Data Base Manager\\cs-db-manager\\new-dbmanager'],
             binaries=[],
             datas=[],
             hiddenimports=['babel.numbers'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='GUI_Controller',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , icon='DBM-Icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='GUI_Controller')

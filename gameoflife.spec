# -*- mode: python -*-

block_cipher = None


a = Analysis(['src/app.py'],
             pathex=['./src'],
             binaries=[],
             datas=[('src/images/*', './images'), ('src/layouts/*', './layouts')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['pep8', 'autopep8', 'pycodestyle'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='GameOfLife',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )

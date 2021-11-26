# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

a = Analysis(['__init__.py'],
             pathex=['C:\\Users\\patryk.morawski\\Documents\\Coding\\Blurr\\BLURR'],
             binaries=[],
             datas=[('.\\face_recognition_models\\models\\dlib_face_recognition_resnet_model_v1.dat', './face_recognition_models/models'),
                    ('.\\face_recognition_models\\models\\mmod_human_face_detector.dat', './face_recognition_models/models'),
                    ('.\\face_recognition_models\\models\\shape_predictor_5_face_landmarks.dat', './face_recognition_models/models'),
                    ('.\\face_recognition_models\\models\\shape_predictor_68_face_landmarks.dat', './face_recognition_models/models'),
                    ('.\\models\\deploy.prototxt', './models'),
                    ('.\\Assets\\', './Assets/'),
                    ('.\\models\\res10_300x300_ssd_iter_140000.caffemodel', './models'),
                    ('C:\\Users\\patryk.morawski\\Anaconda3\\lib\\site-packages\\eel\\eel.js', 'eel'), ('.\\SettingsWindow\\web\\', './SettingsWindow/web/')],
             hiddenimports=['bottle_websocket'],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Blurr',
          debug=True,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )

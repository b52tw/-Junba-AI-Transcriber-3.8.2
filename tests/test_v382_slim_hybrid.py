from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_windows_single_exe_only():
    one = (ROOT / 'JunbaAITranscriber_onefile.spec').read_text(encoding='utf-8')
    yml = (ROOT / '.github/workflows/build-windows-v3.8.yml').read_text(encoding='utf-8')
    assert "name='Junba'" in one
    assert 'Build Single EXE x64' in yml
    assert 'Junba-v382-Single' in yml
    assert 'Build Portable x64' not in yml
    assert 'Junba-v382-Portable' not in yml
    assert 'JunbaAITranscriber_portable.spec' not in yml


def test_android_hybrid_and_key_controls_present():
    main = (ROOT / 'android/app/src/main/java/tw/junba/transcriber/MainActivity.java').read_text(encoding='utf-8')
    gradle = (ROOT / 'android/app/build.gradle.kts').read_text(encoding='utf-8')
    helper = ROOT / 'android/app/src/main/java/tw/junba/transcriber/LocalWhisperEngine.kt'
    secure = ROOT / 'android/app/src/main/java/tw/junba/transcriber/SecureKeyStore.java'
    assert helper.is_file()
    assert secure.is_file()
    assert '自動混合（建議）' in main
    assert '前往 AI Studio 取得 API Key' in main
    assert '從剪貼簿貼上並儲存' in main
    assert 'SecureKeyStore' in main
    assert 'whisper-android:1.0.0' in gradle
    assert 'ffmpeg-kit-audio:8.1.7' in gradle
    assert '**/libc++_shared.so' in gradle
    assert 'LocalWhisperEngine.transcribeAsync' in main
    assert (ROOT / 'android/app/src/main/java/tw/junba/transcriber/AudioPreprocessor.kt').is_file()


def test_workflow_single_artifact_and_android_preflight():
    yml = (ROOT / '.github/workflows/build-windows-v3.8.yml').read_text(encoding='utf-8')
    assert 'Junba-v382-Single' in yml
    assert 'Junba-v382-APK' in yml
    assert 'Junba-v382-Portable' not in yml
    assert ':app:compileDebugKotlin' in yml
    assert "grep -q 'libc++_shared.so'" in yml
    assert "'requirements.txt'" in yml

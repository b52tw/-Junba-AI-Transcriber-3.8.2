# Junba AI Transcriber v3.8.2

本重新封包版只調整 **Junba AI Transcriber v3.8.2** 的建置與 Android 封裝問題；主程式功能不另外重寫。

## 本次修正重點

### Windows：只產出 Single EXE
- GitHub Actions 不再建立 Portable Job。
- Windows Artifact 只會有 `Junba-v382-Single`。
- 內容為 `Junba.exe` + `SHA256.txt`。
- `main.py`、`requirements.txt` 均位於 Repository / ZIP 根目錄。
- `actions/setup-python` 不再啟用 pip cache，避免 `requirements.txt` 若缺漏時在 Source preflight 前就先中止。
- Windows Source preflight 會明確檢查 `main.py`、`requirements.txt`、`app/`、`tests/`、`hooks/`、`packaging/`、`JunbaAITranscriber_onefile.spec`。

### Android：Whisper + Gemini Hybrid 保留
Android 版保留：
- `自動混合（建議）`
- `本機 Whisper（離線）`
- `Google Gemini（雲端）`
- `前往 AI Studio 取得 API Key`
- `從剪貼簿貼上並儲存`
- Android Keystore 加密保存每台手機自己的 API Key
- 手機／平板響應式介面

本次另在 `android/app/build.gradle.kts` 加入 `libc++_shared.so` 的 `pickFirst` 規則，處理 `whisper-android` 與 `ffmpeg-kit-audio` 同時封裝 Native runtime 時的衝突，讓 `assembleDebug` 能繼續完成。

## GitHub Actions
Workflow：

```text
.github/workflows/build-windows-v3.8.yml
```

成功後只會看到這兩個主要 Artifact：

```text
Junba-v382-Single
Junba-v382-APK
```

內容：
- Single：`Junba.exe` + `SHA256.txt`
- APK：`Junba.apk` + `SHA256.txt`

**不會再產出 Portable。**

## Windows 既有功能保留
- faster-whisper / Whisper large-v3
- Intel OpenVINO / Intel GPU/NPU / CPU 自適應
- NVIDIA CUDA 路徑
- Google Gemini
- 批次辨識與自動切段
- Word / TXT / Markdown / SRT / VTT
- Word 時間軸逐字稿
- 每支原始音檔獨立輸出資料夾
- KTV / HTML 錄音核對播放器
- 暫停、繼續、立即停止並輸出目前結果

## Android 本機 Whisper
Android 本機 Whisper 使用 `dev.ffmpegkit-maintained:whisper-android:1.0.0`，另以 `ffmpeg-kit-audio:8.1.7` 在手機本機轉成 Whisper 所需音訊格式。模型不塞進 APK，仍由 App 下載／準備後存於 App 私人目錄。

詳見 `THIRD_PARTY_ANDROID.txt`。

## 上傳 GitHub 前請確認
ZIP 解壓後第一層必須直接看到：

```text
main.py
requirements.txt
JunbaAITranscriber_onefile.spec
app/
android/
hooks/
packaging/
tests/
.github/
```

不要只挑資料夾上傳，也不要漏掉根目錄檔案。

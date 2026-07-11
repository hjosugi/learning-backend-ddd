<!-- i18n: language-switcher -->
[English](README.md) | [日本語](README.ja.md)

# Task API Stdlib

フレームワークのセットアップなしでリクエスト処理、ドメイン関数、JSONレスポンスを示す小さなバックエンドプロジェクト。

## デモを実行する

```bash
python3 projects/task-api-stdlib/app.py --demo
```

## サーバーを起動する

```bash
python3 projects/task-api-stdlib/app.py
```

次に以下を呼び出します：

```bash
curl http://localhost:8080/healthz
curl http://localhost:8080/tasks
curl -X POST http://localhost:8080/tasks -d '{"title":"Write validation test"}'
```

## ドメインロジックをテストする

```bash
python3 projects/task-api-stdlib/test_domain.py
```
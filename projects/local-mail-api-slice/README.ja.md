<!-- i18n: language-switcher -->
[English](README.md) | [日本語](README.ja.md)

# ローカルメールAPIスライス

ローカルのメール送信APIのための最小限のJavaスライス。

これは、古い `local-mail-api` アイデアのDocker不要、フレームワークフリー版です：
送信メールリクエストを検証し、アプリケーションサービスを通して処理し、
配信されたメッセージをテストが検査できるインメモリのメールボックスに保存します。

## 実行方法

```bash
cd projects/local-mail-api-slice
javac *.java
java MailApiTest
rm -f *.class
```

## アップグレードパス

境界が明確になったら、Spring Bootアダプターを追加します：

- コントローラー: `POST /api/mail/send`
- サービス: `MailService` を維持
- インフラストラクチャ: `InMemoryMailbox` を JavaMailSender + GreenMail に置き換え
- テスト: HTTP経由で送信し、メールボックスがメッセージを受信したことをアサートする
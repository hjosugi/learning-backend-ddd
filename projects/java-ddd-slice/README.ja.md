<!-- i18n: language-switcher -->
[English](README.md) | [日本語](README.ja.md)

# Java DDD Slice

フレームワークなしで値オブジェクト、アグリゲートの振る舞い、テストを実装した実行可能なJava 21ドメインスライス。

## テストの実行

```bash
cd projects/java-ddd-slice
javac *.java
java TaskPolicyTest
rm -f *.class
```

## 学べること

- フレームワークコードより前にドメインルールを置くこと
- 値オブジェクトにJavaレコードを使うこと
- ビルドツールのセットアップなしで小さな実行可能テストを書くこと
- 後からSpring BootコントローラーやJPA/R2DBCアダプターへの移行パス
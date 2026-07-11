<!-- i18n: language-switcher -->
[English](repository-profile.md) | [日本語](repository-profile.ja.md)

# リポジトリプロフィール: learning-backend-ddd

最終確認日: 2026-06-20

## GitHub説明

Spring Boot、Quarkus、Go、Phoenix、TypeScriptを横断したバックエンドとDDD学習用リポジトリ。

## トピック

- `learning`
- `java`
- `spring-boot`
- `quarkus`
- `go`
- `ddd`

## 対象読者

複数のフレームワークにおけるバックエンドアーキテクチャ、API設計、永続化、テスト、DDD用語を比較したいエンジニア。

## ソースリポジトリ

- `flux-sample`
- `tasklist`
- `ddd-spring-boot`
- `quarkus-ddd`
- `gin-sample`
- `realworld-phx`
- `ts-ddd`
- `java-sandbox`
- `local-mail-api`

## 最初のマイルストーン

1. Spring MVC/JPAのレッスンを追加する。
2. WebFlux/R2DBCのレッスンを追加する。
3. ハンドラー/サービス/リポジトリの境界を持つGo/Ginのレッスンを追加する。
4. 言語横断で共有するDDD用語表を追加する。
5. `local-mail-api`をローカル開発および統合テストのレッスンとして追加する。

## 公共安全チェックリスト

- データベースダンプや本番接続文字列は含まれていない。
- すべてのサービスにローカル実行手順がある。
- すべてのレッスンにテストまたはチェックコマンドがある。
- メールの例はローカル/テスト用の認証情報のみを使用している。
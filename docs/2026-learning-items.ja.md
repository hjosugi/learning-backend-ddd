<!-- i18n: language-switcher -->
[English](2026-learning-items.md) | [日本語](2026-learning-items.ja.md)

# 2026年の学習項目：バックエンドとDDD

最終確認日：2026-06-20

## 必須学習項目

### API設計

- リクエスト/レスポンスモデル
- バリデーションエラー
- ページネーションとフィルタリング
- 冪等性
- 認証境界
- OpenAPIドキュメント

プロジェクト：

- `tasklist` を `apps/spring-tasklist` に移動する。
- `gin-sample` を `apps/gin-api` に移動する。

### Spring Boot 4 と Java

- Spring Boot 4.1
- Java 21/25
- Spring MVC/JPA
- WebFlux/R2DBC
- Spring Modulithの基礎
- Actuatorのヘルスとメトリクス

プロジェクト：

- `ddd-spring-boot` を `apps/spring-ddd` に移動する。
- `flux-sample` を `apps/spring-webflux-r2dbc` に移動する。

### ローカル開発サービス

- ローカル統合テスト用の組み込みサービス
- プロファイル分離
- テスト専用依存関係
- ローカル開発に外部認証情報を使わない

プロジェクト：

- `local-mail-api` を `apps/local-mail-api` または `lessons/local-mail-api` に移動する。
- Spring Boot + GreenMailのレッスンとして利用する。

### DDDとアーキテクチャ

- エンティティ
- 値オブジェクト
- アグリゲート
- リポジトリ
- アプリケーションサービス
- ドメインイベント
- モジュール境界
- アンチコロージョンレイヤー

プロジェクト：

- `docs/ddd-vocabulary.md` を追加する。
- 同じユースケースをSpring、Quarkus、Goで追加する。

### フレームワーク比較

- Spring Boot
- Quarkus
- Go/Gin
- Phoenix
- TypeScriptサービスモデル

プロジェクト：

- `quarkus-ddd` を `apps/quarkus-ddd` に移動する。
- `realworld-phx` は `reading/phoenix-realworld` として保持する。

## 完了の定義

- すべてのアプリに実行コマンドがあること。
- すべてのアプリに少なくとも1つの統合テストまたはドキュメント化された手動curlフローがあること。
- すべてのアプリにローカル依存関係がドキュメント化されていること。
- すべてのフレームワーク比較にトレードオフが含まれていること。
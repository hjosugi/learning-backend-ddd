<!-- i18n: language-switcher -->
[English](README.md) | [日本語](README.ja.md)

# バックエンドDDD学習

Spring Boot、Quarkus、Go/Gin、Phoenix、TypeScriptサービスパターン、およびローカル開発サービスを横断したバックエンドとDDDの学習パス。

最終確認日: 2026-06-21

## 開発環境

ローカルにGo、Java、Node.js、またはPythonがない場合は、Nixシェルに入ってください：

```bash
nix develop
```

## 実行可能なスタータープロジェクト

Spring、Quarkus、Go、またはPhoenixに進む前に、小さなJSONタスクAPIを実行してください：

```bash
python3 projects/task-api-stdlib/app.py --demo
python3 projects/task-api-stdlib/test_domain.py
```

HTTPサーバーを起動するには：

```bash
python3 projects/task-api-stdlib/app.py
```

## 対象ハンズオンプロジェクト

これらのプロジェクトは、単なるメモではなく実際のバックエンド学習対象を使用しています：

```bash
cd projects/go-http-api
go test ./...
```

```bash
cd projects/java-ddd-slice
javac *.java
java TaskPolicyTest
rm -f *.class
```

`apps/spring-ddd`に対応するstdlibのDDD戦術コア（Orders境界コンテキスト）：

```bash
python3 projects/ddd-tactical-core/orders.py --demo
cd projects/ddd-tactical-core && python3 -m unittest -v
```

API登録なしのGraphQL：

```bash
node projects/graphql-local-api/server.test.mjs
```

ローカルメールAPI境界：

```bash
cd projects/local-mail-api-slice
javac *.java
java MailApiTest
rm -f *.class
```

これらのスライスを使って、ハンドラー境界、JSON契約、Javaドメインモデリング、DDD戦術パターン（エンティティ、値オブジェクト、アグリゲート、リポジトリ、アプリケーションサービス、ドメインイベント）、GraphQLリゾルバーの形状、ローカルサービスのダブル、Spring Boot、Quarkus、Apollo、GraphQL Yoga、GreenMailアダプターを追加する前に存在すべきコードを学びます。

キュレーションされたDDDおよびSpring Bootの参考資料は[docs/learning-resources.md](docs/learning-resources.md)を参照してください。

## ベースライン

- ローカルデフォルトはJava 21、利用可能な場合はJava 25 LTSをターゲット
- 新しいSpring例にはSpring Boot 4.1.0
- Go 1.26.x
- PostgreSQL指向の永続化例
- 有用な場合はOpenAPI/リクエスト-レスポンス例

## このリポジトリで学べること

このリポジトリは、小さな実行可能サービスを通じたバックエンドシステム設計のためのものです。

例は以下の関心事を可視化します：

- リクエスト/レスポンス契約とバリデーションエラー
- トランザクション境界と永続化のトレードオフ
- DDD用語がコードを明確にする箇所と儀式的になる箇所
- 統合テストのためのローカル依存戦略
- Spring Boot、Quarkus、Go/Gin、Phoenix、TypeScriptサービスコード間のフレームワークの違い
- ヘルスチェック、メトリクス、構造化ログなどの運用フック

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

## 学習パス

1. REST APIの基本
2. バリデーションとエラー応答
3. 永続化とトランザクション
4. DDD用語
5. Spring MVC/JPA
6. WebFlux/R2DBC
7. Quarkus
8. Go/Gin
9. Phoenixアーキテクチャの読解
10. GreenMailなどのローカル開発サービス

## 予定構成

```text
apps/
  spring-tasklist/
  spring-ddd/
  spring-webflux-r2dbc/
  quarkus-ddd/
  gin-api/
  local-mail-api/
reading/
  phoenix-realworld/
docs/
  2026-learning-items.md
  ddd-vocabulary.md
  framework-comparison.md
  repository-profile.md
```

## 学習ループ

1. 1つのユースケースから始めてAPI契約を書く
2. 1つのフレームワークで実装する
3. バリデーション、永続化、テスト可能なローカル依存を追加する
4. そのスライスで使われるDDD用語を書く
5. 最初のフレームワークが理解できてから別のフレームワークの同じスライスを比較する

## 他に属するもの

- データベースカタログ実験は`learning-data-stores`に属する
- フロントエンドクライアントは`learning-frontend-typescript`に属する
- CI、NGINX、デプロイ、可観測性テンプレートは`learning-platform-engineering`に属する
- セキュリティテストラボは`learning-security-labs`に属する

## リポジトリプロフィール

GitHubの説明、トピック、公的安全ノート、最初のマイルストーンは[docs/repository-profile.md](docs/repository-profile.md)を参照してください。

## ライセンス

0BSD。このプロジェクトはほぼあらゆる目的で使用、コピー、改変、配布が可能です。
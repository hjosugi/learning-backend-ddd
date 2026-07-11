<!-- i18n: language-switcher -->
[English](README.md) | [日本語](README.ja.md)

# GraphQL ローカルAPI

ホストされたAPIキーやフレームワークの依存なしに、GraphQLのリクエスト形状、リゾルバの境界、レスポンス契約を学びましょう。

これは意図的に小さく作られたGraphQL風のラボです。完全なGraphQL実装ではありません。Apollo Server、GraphQL Yoga、Spring for GraphQL、またはフェデレーションツールを追加する前に、動作の仕組みを理解するために使ってください。

## 実行

```bash
node projects/graphql-local-api/server.test.mjs
node projects/graphql-local-api/server.mjs
```

リクエスト例:

```bash
curl -s http://127.0.0.1:8788/graphql \
  -H 'content-type: application/json' \
  -d '{"query":"{ books { id title author } }"}'
```

## 注目すべき点

- HTTPエンドポイントは安定しています：`POST /graphql`。
- リゾルバがどのアプリケーションデータを公開するかを決定します。
- クライアントはフィールドを選択するため、バックエンドコードは部分的なレスポンスを意図的に処理する必要があります。
- バリデーション、変数、イントロスペクション、バッチ処理、認証、永続化クエリは、実際のGraphQLライブラリで追加すべき次のトピックです。
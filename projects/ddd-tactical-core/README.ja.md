<!-- i18n: language-switcher -->
[English](README.md) | [日本語](README.ja.md)

# DDD タクティカルコア

純粋な Python（標準ライブラリのみ、フレームワークなし）で **DDD タクティカルパターン** を使って構築された小さな **Orders** バウンデッドコンテキストです。これは、値オブジェクト、エンティティ、アグリゲートルート、リポジトリ、アプリケーションサービス、ドメインイベントといった語彙を、Spring Boot に移植する *前に* 一度に読み書きできるコードで体感できるように存在しています。

これは `apps/spring-ddd` が目指す標準ライブラリ版です。

最終検証日: 2026-06-21

## ここに含まれるもの

| ファイル | タクティカルパターン |
| --- | --- |
| `orders.py` `Money` | 値オブジェクト：不変、通貨対応、値による等価性、負値を拒否 |
| `orders.py` `OrderLine` | アグリゲート内に保持される値オブジェクト；小計は派生 |
| `orders.py` `Order` | アグリゲートルート：識別子、不変条件、再計算される合計、ドメインイベントを発行 |
| `orders.py` `OrderConfirmed` | ドメインイベント（過去形、不変） |
| `orders.py` `OrderRepository` / `InMemoryOrderRepository` | リポジトリ：`Protocol` インターフェース + メモリ内実装 |
| `orders.py` `PlaceOrder` | アプリケーションサービス / ユースケース + イベントの購読者へのディスパッチ |
| `test_orders.py` | 上記すべてをカバーする `unittest` テストスイート |

`Order` アグリゲートに課される不変条件:

- **空の**注文は確定できない
- **合計**は常に行から再計算され、保存されたフィールドではない
- 確定後は**変更禁止**（追加・削除・確定はすべて拒否）
- 行の通貨は注文の通貨と一致しなければならない
- 既存のSKUを追加すると数量がマージされ、重複しない

## 実行

```bash
python3 projects/ddd-tactical-core/orders.py --demo
```

これは `PlaceOrder` ユースケースをエンドツーエンドで実行します：ドラフト作成、2つの行アイテム追加、確定、そして `OrderConfirmed` ドメインイベントが購読者にディスパッチされる様子を確認できます。

## テスト

非対話的で、失敗時は非ゼロ終了コードを返します（CIゲートとして機能します）：

```bash
cd projects/ddd-tactical-core && python3 -m unittest -v
```

## アップグレードパス

このプロジェクトは意図的にフレームワークフリーです。各タクティカルパーツは **Spring Boot 4** (`apps/spring-ddd`) の対応物に直接マッピングされます。Spring版を構築するときは、各標準ライブラリの継ぎ目を以下の実際のツールに置き換えます — ドメインの形は変わりません。

| 本プロジェクト（標準ライブラリ） | Spring Boot 4 対応物 |
| --- | --- |
| `Money` 不変データクラス | `@Embeddable` 値型（例：`@Embeddable` / `@AttributeOverride` でマッピングされた Java の `record`）、エンティティに埋め込み |
| `Order` アグリゲートルート（プレーンクラス） | `@Entity` と `@Id`；行は `@OneToMany` / `@ElementCollection`；不変条件はサービスではなくエンティティ内に保持 |
| `OrderLine` 値オブジェクト | `@ElementCollection` 内の `@Embeddable`、またはアグリゲートが所有する子 `@Entity` |
| 再計算される `total()` | `@Transient` / 派生ゲッター、またはドメインメソッド内で計算 — 永続化フィールドとしては持たずズレを防止 |
| `OrderRepository` `Protocol` + `InMemoryOrderRepository` | `interface OrderRepository extends JpaRepository<Order, UUID>`（Spring Data が実装生成）；メモリ内マップを PostgreSQL に置き換え |
| `OrderConfirmed` ドメインイベント | プレーンなイベントクラス；`AbstractAggregateRoot.registerEvent(...)` で発行、またはドメインから返す |
| `order.pull_events()` + `PlaceOrder._dispatch` | `ApplicationEventPublisher.publishEvent(...)`、または Spring Data の `@DomainEvents` / `@AfterDomainEventPublication` による `save` 時の自動発行 |
| 購読者コール可能オブジェクト (`use_case.subscribe`) | `@EventListener` / `@TransactionalEventListener(phase = AFTER_COMMIT)` の Bean |
| `PlaceOrder` アプリケーションサービス | リポジトリ経由でロードしドメインメソッドを呼び、コミット時にイベントを発行する `@Service @Transactional` クラス |
| `python3 -m unittest` | JUnit 5 + `@DataJpaTest` / `@SpringBootTest`、統合テストには Testcontainers PostgreSQL を使用 |

テストを常に成功させながら移行する順序:

1. `Money`、`OrderLine`、`Order`、`OrderConfirmed` をプレーンな Java クラス/レコードとして JUnit テスト付きで移植（まだ Spring は使わない） — これは `projects/java-ddd-slice` スタイル。
2. JPA アノテーションと Spring Data の `OrderRepository` を追加；ユニットテスト用にメモリ内フェイクを維持し、統合テストには Testcontainers を使用。
3. 手動イベントディスパッチを `ApplicationEventPublisher` / `@TransactionalEventListener(AFTER_COMMIT)` に置き換え。
4. ユースケースを `@Service @Transactional` でラップし、`apps/spring-ddd` のコントローラ経由で公開。

## 演習

モデルを深めるための具体的な次のステップ（それぞれ小さく独立した PR）:

1. **`OrderCancelled` ドメインイベントを追加。** `Order.cancel()` を実装し、*確定済み* 注文はキャンセル可能だがドラフトは不可という不変条件を設け、イベントを発行し、`PlaceOrder` に購読者を追加、両パスのテストを作成。
2. **`Quantity` 値オブジェクトを導入。** `OrderLine` の生の `int` 数量を、0 以下を拒否し最大値（例：999）で上限を設ける `Quantity` 値オブジェクトに置き換え。不変条件が値オブジェクト側に移動し、値による等価性が保たれることを示す。
3. **アグリゲートサイズの不変条件を強制。** `add_line` で異なる行アイテム数が N を超える注文を拒否し、アグリゲートが整合性境界内に収まることを証明するテストを追加。
4. **実用的な永続化継ぎ目を追加。** 2つ目のリポジトリ実装 `JsonFileOrderRepository` を作成し、注文を `/tmp` 以下の JSON ファイルにシリアライズ（標準ライブラリの `json` のみ使用）。両実装に対して同じ `PlaceOrder` テストを再実行し、ドメインがストレージに依存しないことを証明。
5. **イベント発行をトランザクション化。** `PlaceOrder.confirm` を変更し、`repository.save` が例外を投げた場合は *一切* イベントを発行しない（コミット後発行のセマンティクス）。失敗する保存を投げるフェイクリポジトリを使ったテストを追加。
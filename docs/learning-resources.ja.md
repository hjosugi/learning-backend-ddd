<!-- i18n: language-switcher -->
[English](learning-resources.md) | [日本語](learning-resources.ja.md)

# さらなる学習リソース

最終確認日: 2026-06-21

このリポジトリの名前付き学習技術に関する厳選された正典的な一次資料：
**DDD戦術パターン**（エンティティ、値オブジェクト、アグリゲート、リポジトリ、
アプリケーションサービス、ドメインイベント）と、それらが移植される**Spring Boot / Java**スタック。リンクは深い推測パスよりもドキュメントのルートを優先しています。

## DDD戦術パターン

- **Domain-Driven Design: Tackling Complexity in the Heart of Software** -- Eric Evans（「青本」）。
  <https://www.domainlanguage.com/ddd/>
  エンティティ、値オブジェクト、アグリゲート、リポジトリ、ドメインイベントの
  オリジナルソース。このリポジトリ全体の語彙の基盤。

- **Implementing Domain-Driven Design** -- Vaughn Vernon（「赤本」）。
  <https://www.informit.com/store/implementing-domain-driven-design-9780321834577>
  アグリゲート、リポジトリ、ドメインイベントの最も実践的でコード中心の解説；
  `ddd-tactical-core`を実際に構造化する方法に最も近い。

- **Domain-Driven Design Reference** -- Eric Evans（無料の簡潔な定義集）。
  <https://www.domainlanguage.com/ddd/reference/>
  戦術的ビルディングブロックの短く権威ある用語集 — 「アグリゲートルート」や「値オブジェクト」の
  正確な定義が欲しいときに最適。

- **DDD Aggregate** -- Martin Fowler。
  <https://martinfowler.com/bliki/DDD_Aggregate.html>
  アグリゲート境界とルートが唯一のエントリポイントである理由の明快で広く引用される説明 —
  `Order`クラスが強制する不変条件とまさに一致。

## Spring Boot / Java（アップグレード対象）

- **Spring Boot リファレンスドキュメント**。
  <https://docs.spring.io/spring-boot/>
  フレームワークの公式ドキュメント。`apps/spring-ddd`で使用される；
  `@Service`、設定、テストスライスの開始点。

- **Spring Data JPA リファレンス**。
  <https://spring.io/projects/spring-data-jpa>
  リポジトリ抽象化（`JpaRepository`）および集約イベントの保存時自動公開のための
  `@DomainEvents` / `@AfterDomainEventPublication`。

- **Spring Framework リファレンス — アプリケーションイベント**。
  <https://docs.spring.io/spring-framework/reference/>
  `ApplicationEventPublisher`、`@EventListener`、`@TransactionalEventListener` —
  本プロジェクトの手動`subscribe` / `_dispatch`イベント機構の実運用置き換え。

- **Spring Modulith**。
  <https://spring.io/projects/spring-modulith>
  境界づけられたコンテキスト間のモジュール境界とイベント駆動型通信；
  単一の戦術コアの次の自然なステップ。

- **Jakarta Persistence (JPA) 仕様**。
  <https://jakarta.ee/specifications/persistence/>
  Spring移植でアグリゲートや値オブジェクトのマッピングに使われる
  `@Entity`、`@Embeddable`、`@ElementCollection`の標準。

## Python（この実装）

- **Python `dataclasses` ドキュメント**。
  <https://docs.python.org/3/library/dataclasses.html>
  値の等価性とハッシュを持つ不変の値オブジェクトのための`frozen=True` —
  `Money`や`OrderLine`の基礎。

- **Python `unittest` ドキュメント**。
  <https://docs.python.org/3/library/unittest.html>
  `test_orders.py`で使われている標準ライブラリのテストフレームワーク；
  Spring移植のJUnit 5の概念的な類似物。

- **Python `typing.Protocol`**。
  <https://docs.python.org/3/library/typing.html>
  継承なしで`OrderRepository`を定義するための構造的インターフェース —
  後にSpring Dataが実装する継ぎ目。
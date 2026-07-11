<!-- i18n: language-switcher -->
[English](README.md) | [日本語](README.ja.md)

# Java DDD Slice

Runnable Java 21 domain slice for value objects, aggregate behavior, and tests without a framework.

## Run Test

```bash
cd projects/java-ddd-slice
javac *.java
java TaskPolicyTest
rm -f *.class
```

## What To Learn

- domain rules before framework code
- Java records for value objects
- small executable tests without build-tool setup
- later migration path to Spring Boot controllers and JPA/R2DBC adapters


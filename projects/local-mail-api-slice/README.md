# Local Mail API Slice

Minimal Java slice for a local mail-sending API.

This is the Dockerless, framework-free version of the old `local-mail-api` idea:
validate a send-mail request, pass it through an application service, and store
the delivered message in an in-memory mailbox that tests can inspect.

## Run

```bash
cd projects/local-mail-api-slice
javac *.java
java MailApiTest
rm -f *.class
```

## Upgrade Path

After the boundary is clear, add a Spring Boot adapter:

- controller: `POST /api/mail/send`
- service: keep `MailService`
- infrastructure: replace `InMemoryMailbox` with JavaMailSender + GreenMail
- test: send through HTTP, then assert the mailbox received the message

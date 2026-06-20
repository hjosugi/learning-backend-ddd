import java.time.Instant;
import java.util.ArrayList;
import java.util.List;

record SendMailRequest(String to, String subject, String text) {
}

record SendMailResponse(String status, String to) {
}

record DeliveredMail(String from, String to, String subject, String body, Instant deliveredAt) {
}

interface Mailbox {
    void deliver(DeliveredMail mail);

    List<DeliveredMail> all();
}

final class InMemoryMailbox implements Mailbox {
    private final List<DeliveredMail> messages = new ArrayList<>();

    @Override
    public void deliver(DeliveredMail mail) {
        messages.add(mail);
    }

    @Override
    public List<DeliveredMail> all() {
        return List.copyOf(messages);
    }
}

final class MailService {
    private final Mailbox mailbox;
    private final String from;

    MailService(Mailbox mailbox, String from) {
        this.mailbox = mailbox;
        this.from = from;
    }

    SendMailResponse send(SendMailRequest request) {
        validate(request);
        mailbox.deliver(new DeliveredMail(
            from,
            request.to(),
            request.subject(),
            request.text() == null ? "" : request.text(),
            Instant.now()
        ));
        return new SendMailResponse("sent", request.to());
    }

    private static void validate(SendMailRequest request) {
        if (request.to() == null || request.to().isBlank()) {
            throw new IllegalArgumentException("to is required");
        }
        if (request.subject() == null || request.subject().isBlank()) {
            throw new IllegalArgumentException("subject is required");
        }
    }
}

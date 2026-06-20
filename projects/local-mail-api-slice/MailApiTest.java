import java.util.List;

public class MailApiTest {
    public static void main(String[] args) {
        InMemoryMailbox mailbox = new InMemoryMailbox();
        MailService service = new MailService(mailbox, "no-reply@demo.local");

        SendMailRequest request = new SendMailRequest("bob@demo.local", "Hello", "Body");
        SendMailResponse response = service.send(request);

        assertEquals("sent", response.status());
        assertEquals("bob@demo.local", response.to());

        List<DeliveredMail> delivered = mailbox.all();
        assertEquals(1, delivered.size());
        assertEquals("no-reply@demo.local", delivered.getFirst().from());
        assertEquals("Hello", delivered.getFirst().subject());

        assertThrows(() -> service.send(new SendMailRequest("", "Hello", "Body")));
        assertThrows(() -> service.send(new SendMailRequest("bob@demo.local", "", "Body")));

        System.out.println("ok");
    }

    private static void assertEquals(Object expected, Object actual) {
        if (!expected.equals(actual)) {
            throw new AssertionError("expected " + expected + " but got " + actual);
        }
    }

    private static void assertThrows(Runnable runnable) {
        try {
            runnable.run();
        } catch (IllegalArgumentException expected) {
            return;
        }
        throw new AssertionError("expected IllegalArgumentException");
    }
}

public class TaskPolicyTest {
  public static void main(String[] args) {
    Task urgent = new Task("Ship backend slice", Priority.HIGH, false);
    assertTrue(TaskPolicy.needsReview(urgent), "high open task needs review");

    Task done = urgent.complete();
    assertFalse(TaskPolicy.needsReview(done), "done task does not need review");

    try {
      new Task("x", Priority.LOW, false);
      throw new AssertionError("expected validation error");
    } catch (IllegalArgumentException expected) {
      assertTrue(expected.getMessage().contains("title"), "error mentions title");
    }

    System.out.println("ok");
  }

  private static void assertTrue(boolean value, String message) {
    if (!value) {
      throw new AssertionError(message);
    }
  }

  private static void assertFalse(boolean value, String message) {
    assertTrue(!value, message);
  }
}


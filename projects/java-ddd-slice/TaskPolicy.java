public final class TaskPolicy {
  private TaskPolicy() {}

  public static boolean needsReview(Task task) {
    return task.priority() == Priority.HIGH && !task.done();
  }
}


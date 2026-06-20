public record Task(String title, Priority priority, boolean done) {
  public Task {
    if (title == null || title.trim().length() < 3) {
      throw new IllegalArgumentException("title must be at least 3 characters");
    }
  }

  public Task complete() {
    return new Task(title, priority, true);
  }
}

enum Priority {
  LOW,
  NORMAL,
  HIGH
}


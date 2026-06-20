import http from "node:http";

const books = [
  { id: "b1", title: "Domain Modeling Made Functional", author: "Scott Wlaschin" },
  { id: "b2", title: "Designing Data-Intensive Applications", author: "Martin Kleppmann" },
];

function fieldsFor(query, fieldName) {
  const match = query.match(new RegExp(`${fieldName}(?:\\s*\\([^)]*\\))?\\s*\\{([^}]+)\\}`, "s"));
  if (!match) {
    return [];
  }
  return match[1].split(/\s+/).map((field) => field.trim()).filter(Boolean);
}

function project(record, fields) {
  return Object.fromEntries(fields.map((field) => [field, record[field] ?? null]));
}

export function executeQuery(query) {
  if (typeof query !== "string" || query.trim() === "") {
    return { errors: [{ message: "query is required" }] };
  }

  if (/\bbooks\b/.test(query)) {
    const fields = fieldsFor(query, "books");
    return { data: { books: books.map((book) => project(book, fields)) } };
  }

  if (/\bbook\b/.test(query)) {
    const id = query.match(/book\s*\(\s*id\s*:\s*"([^"]+)"/)?.[1];
    const fields = fieldsFor(query, "book");
    const book = books.find((item) => item.id === id);
    return { data: { book: book ? project(book, fields) : null } };
  }

  return { errors: [{ message: "supported fields: books, book(id)" }] };
}

export function createServer() {
  return http.createServer(async (request, response) => {
    if (request.method !== "POST" || request.url !== "/graphql") {
      response.writeHead(404, { "content-type": "application/json" });
      response.end(JSON.stringify({ errors: [{ message: "not found" }] }));
      return;
    }

    const chunks = [];
    for await (const chunk of request) {
      chunks.push(chunk);
    }

    let body;
    try {
      body = JSON.parse(Buffer.concat(chunks).toString("utf8"));
    } catch {
      response.writeHead(400, { "content-type": "application/json" });
      response.end(JSON.stringify({ errors: [{ message: "invalid json" }] }));
      return;
    }

    response.writeHead(200, { "content-type": "application/json" });
    response.end(JSON.stringify(executeQuery(body.query)));
  });
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const port = Number(process.env.PORT ?? 8788);
  createServer().listen(port, "127.0.0.1", () => {
    console.log(`GraphQL lab listening on http://127.0.0.1:${port}/graphql`);
  });
}

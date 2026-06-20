import assert from "node:assert/strict";
import { executeQuery } from "./server.mjs";

assert.deepEqual(executeQuery("{ books { id title } }"), {
  data: {
    books: [
      { id: "b1", title: "Domain Modeling Made Functional" },
      { id: "b2", title: "Designing Data-Intensive Applications" },
    ],
  },
});

assert.deepEqual(executeQuery('{ book(id: "b2") { title author } }'), {
  data: {
    book: {
      title: "Designing Data-Intensive Applications",
      author: "Martin Kleppmann",
    },
  },
});

assert.deepEqual(executeQuery('{ book(id: "missing") { id title } }'), {
  data: { book: null },
});

assert.equal(executeQuery("{ unknown { id } }").errors[0].message, "supported fields: books, book(id)");
console.log("ok");

import { validate } from "@/lib/validation";

test("validate accepts empty and partial rule maps", () => {
  const form = { a: "1", b: "" };
  expect(validate(form, {})).toEqual({ a: null, b: null });
  const res = validate(form, { b: { type: "required" } });
  expect(res).toEqual({ a: null, b: "This field is required" });
});

test("validate returns first failing rule message", () => {
  const res = validate(
    { a: "" },
    {
      a: [
        { type: "required", message: "req" },
        { type: "regex", pattern: /^a$/, message: "regex" },
      ],
    },
  );
  expect(res.a).toBe("req");

  const res2 = validate(
    { a: "b" },
    {
      a: [
        { type: "required", message: "req" },
        { type: "regex", pattern: /^a$/, message: "regex" },
      ],
    },
  );
  expect(res2.a).toBe("regex");
});

test("validate handles required and regex rules", () => {
  const req = validate({ a: "" }, { a: { type: "required" } });
  expect(req.a).toBe("This field is required");

  const re = validate({ a: "b" }, { a: { type: "regex", pattern: /^a$/, message: "bad" } });
  expect(re.a).toBe("bad");
});

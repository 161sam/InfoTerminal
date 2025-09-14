module.exports = {
  meta: { type: "problem", docs: { description: "Disallow direct host URLs in fetch; use /api/plugins instead" } },
  create(context) {
    return {
      CallExpression(node) {
        if (node.callee.name !== "fetch") return;
        const arg = node.arguments[0];
        if (arg && arg.type === "Literal" && typeof arg.value === "string" && /^https?:\/\//i.test(arg.value)) {
          context.report({ node: arg, message: "Do not hardcode hosts in fetch(). Use relative /api/plugins or API utils." });
        }
      }
    };
  }
};

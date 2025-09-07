export type ValidationRule =
  | { type: 'required'; message?: string }
  | { type: 'regex'; pattern: RegExp; message?: string }
  | { type: 'custom'; validate: (value: unknown, form?: unknown) => boolean | string };

export type ValidatorMap<T> = Partial<Record<keyof T, ValidationRule | ValidationRule[]>>;

function runRule(value: unknown, rule: ValidationRule, form?: Record<string, unknown>): string | null {
  switch (rule.type) {
    case 'required': {
      const empty =
        value === undefined ||
        value === null ||
        (typeof value === 'string' && value.trim() === '');
      return empty ? rule.message ?? 'This field is required' : null;
    }
    case 'regex':
      return typeof value === 'string' && rule.pattern.test(value)
        ? null
        : rule.message ?? 'Invalid format';
    case 'custom': {
      const res = rule.validate(value, form);
      if (res === true) return null;
      if (res === false) return 'Invalid value';
      return res;
    }
    default:
      return null;
  }
}

export function validateField(
  value: unknown,
  rule: ValidationRule | ValidationRule[] | undefined,
  form?: Record<string, unknown>
): string | null {
  if (!rule) return null;
  const rules = Array.isArray(rule) ? rule : [rule];
  for (const r of rules) {
    const msg = runRule(value, r, form);
    if (msg) return msg;
  }
  return null;
}

export function validate<T extends Record<string, unknown>>(
  form: T,
  rules: ValidatorMap<T>
): Record<keyof T, string | null> {
  const result: Record<keyof T, string | null> = {} as any;
  (Object.keys(form) as (keyof T)[]).forEach((key) => {
    result[key] = validateField(form[key], rules[key], form);
  });
  return result;
}

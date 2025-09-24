export type CanonicalRole = "admin" | "ops" | "analyst" | "viewer";

export type RbacFeature = "opsActions" | "pluginRunner" | "videoAnalysis" | "dossierExport";

const ROLE_ALIASES: Record<string, CanonicalRole> = {
  admin: "admin",
  administrator: "admin",
  superadmin: "admin",
  superuser: "admin",
  ops: "ops",
  operator: "ops",
  operations: "ops",
  devops: "ops",
  analyst: "analyst",
  intelligence_analyst: "analyst",
  security_analyst: "analyst",
  investigator: "analyst",
  viewer: "viewer",
  read: "viewer",
  reader: "viewer",
  guest: "viewer",
};

const FEATURE_MATRIX: Record<RbacFeature, CanonicalRole[]> = {
  opsActions: ["admin", "ops"],
  pluginRunner: ["admin", "ops"],
  videoAnalysis: ["admin", "analyst"],
  dossierExport: ["admin", "analyst"],
};

const ROLE_ORDER: CanonicalRole[] = ["admin", "ops", "analyst", "viewer"];

function detectRole(raw: string): CanonicalRole | null {
  if (!raw) return null;
  const normalized = raw.trim().toLowerCase();
  if (!normalized) return null;
  if (ROLE_ALIASES[normalized]) {
    return ROLE_ALIASES[normalized];
  }

  const tokens = normalized.split(/[^a-z0-9]+/).filter(Boolean);
  for (let index = tokens.length - 1; index >= 0; index -= 1) {
    const token = tokens[index];
    if (ROLE_ALIASES[token]) {
      return ROLE_ALIASES[token];
    }
  }

  return null;
}

export function canonicalizeRoles(values: Array<string | null | undefined>): CanonicalRole[] {
  const detected = new Set<CanonicalRole>();
  values.forEach((value) => {
    if (typeof value !== "string") return;
    const role = detectRole(value);
    if (role) {
      detected.add(role);
    }
  });

  if (detected.size === 0) {
    detected.add("viewer");
  }

  return ROLE_ORDER.filter((role) => detected.has(role));
}

export function canAccessFeature(
  roles: Array<string | null | undefined> | null | undefined,
  feature: RbacFeature,
): boolean {
  const canonical = canonicalizeRoles(Array.isArray(roles) ? roles : []);
  const allowed = FEATURE_MATRIX[feature];
  return allowed.some((role) => canonical.includes(role));
}

export function summarizeFeatureAccess(roles: Array<string | null | undefined> | null | undefined) {
  return {
    opsActions: canAccessFeature(roles, "opsActions"),
    pluginRunner: canAccessFeature(roles, "pluginRunner"),
    videoAnalysis: canAccessFeature(roles, "videoAnalysis"),
    dossierExport: canAccessFeature(roles, "dossierExport"),
  };
}

export { FEATURE_MATRIX };

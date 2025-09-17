# Auth Scripts

Keycloak Realm Import (kcadm)
-----------------------------

Use the helper script to import/update the `infoterminal` realm:

1) Ensure Keycloak is running at `IT_OIDC_ISSUER` (default http://localhost:8643)
2) Run the script (idempotent):

   bash scripts/keycloak_kcadm_import.sh

Options (env):
- `KC_URL` (default `http://localhost:8643`)
- `KC_REALM_FILE` (default `infra/keycloak/realm-infoterminal.json`)
- `KC_ADMIN`/`KC_PASS` (default `admin`/`adminadmin`)
- `DRY_RUN=1` to print commands without applying

The script uses a temporary Keycloak container to run `kcadm.sh` and upserts the realm.

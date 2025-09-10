- ACTION: mkdir
  DST: docs/architecture/diagrams
  WHY: ensure structure
- ACTION: mkdir
  DST: docs/dev/guides
  WHY: ensure structure
- ACTION: mkdir
  DST: docs/dev/research
  WHY: ensure structure
- ACTION: mkdir
  DST: docs/dev/roadmap/v0.3-plus
  WHY: ensure structure
- ACTION: mkdir
  DST: docs/integrations
  WHY: ensure structure
- ACTION: mkdir
  DST: docs/presets/waveterm
  WHY: ensure structure
- ACTION: move
  SRC: docs/testing.md
  DST: docs/dev/guides/testing.md
  WHY: structure
  DIFF: moved
- ACTION: move
  SRC: docs/dev/RAG-Systeme.md
  DST: docs/dev/guides/rag-systems.md
  WHY: structure
  DIFF: moved
- ACTION: move
  SRC: docs/dev/Frontend-Modernisierung.md
  DST: docs/dev/guides/frontend-modernization.md
  WHY: structure
  DIFF: moved
- ACTION: move
  SRC: docs/dev/Frontend-Modernisierung_Setup-Guide.md
  DST: docs/dev/guides/frontend-modernization-setup-guide.md
  WHY: structure
  DIFF: moved
- ACTION: move
  SRC: docs/dev/ROADMAPv0.1.0.md
  DST: docs/dev/roadmap/v0.1-overview.md
  WHY: structure
  DIFF: moved
- ACTION: move
  SRC: docs/dev/Release-Planv0.2-v1.0.md
  DST: docs/dev/roadmap/v0.2-overview.md
  WHY: structure
  DIFF: moved
- ACTION: move
  SRC: docs/runbooks/RUNBOOK-obs-opa-secrets.md
  DST: docs/runbooks/obs-opa-secrets.md
  WHY: naming
  DIFF: moved
- ACTION: merge
  SRC: docs/runbooks/RUNBOOK-stack.md & docs/OPERABILITY.md
  DST: docs/runbooks/stack.md
  WHY: runbooks
  DIFF: merged
- ACTION: merge+link
  SRC: docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md#L1-L3
  DST: docs/dev/guides/flowise-agents.md#docs-blueprints-flowise-agents-blueprint-md
  WHY: deduplicate
  HASH: 51c326eccacbf2d88a42a1fe24b7d68384255acb
- ACTION: merge+link
  SRC: docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md#L88-L89
  DST: docs/dev/guides/flowise-agents.md#agent-gateway-api
  WHY: deduplicate
  HASH: d0eaaa31c2898c408446649d88f6da93a5333289
- ACTION: merge+link
  SRC: docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md#L156-L157
  DST: docs/dev/guides/flowise-agents.md#
  WHY: deduplicate
  HASH: 028096ac140d4eabf9edd35c0bd7e5941292a0c2
- ACTION: merge+link
  SRC: docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md#L205-L206
  DST: docs/dev/guides/flowise-agents.md#zweck
  WHY: deduplicate
  HASH: 319b5ae6459d8708cf583ad2dd77aee57455f16b
- ACTION: merge+link
  SRC: docs/adr/0002-multi-storage-pattern.md#L1-L4
  DST: docs/dev/guides/rag-systems.md#adr-0002-multi-storage-pattern
  WHY: deduplicate
  HASH: 48abbf4672d83d2600f286eba1f7bc22ed7289d0
- ACTION: merge+link
  SRC: docs/adr/0002-multi-storage-pattern.md#L5-L8
  DST: docs/dev/guides/rag-systems.md#
  WHY: deduplicate
  HASH: 8fbddc15c894c9dc8fa1dcf050754ca02f880efe
- ACTION: merge+link
  SRC: docs/dev/frontend_modernization_guide.md#L1-L2
  DST: docs/dev/guides/frontend-modernization.md#markdownlint-disable-md013
  WHY: deduplicate
  HASH: f30bd0996b1a4a5356bcd88f0df8f63d34e7474d
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L55-L57
  DST: docs/dev/guides/frontend-modernization.md#2-dependencies-installieren
  WHY: deduplicate
  HASH: c6e8e65acff9597df6a94e14f79200856c07e163
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L68-L70
  DST: docs/dev/guides/frontend-modernization.md#bash
  WHY: deduplicate
  HASH: d0360679ce03420e82b67b3a400e93563bf3a441
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L202-L204
  DST: docs/dev/guides/frontend-modernization.md#next-public-search-api-http-localhost-8001
  WHY: deduplicate
  HASH: de927ab690e194c5a6fe8744682adb93e08c7bcd
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L261-L263
  DST: docs/dev/guides/frontend-modernization.md#type-check
  WHY: deduplicate
  HASH: 1e299693cdffeb846964401658e292b3d9d1a3ff
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L382-L384
  DST: docs/dev/guides/frontend-modernization.md#npm-install
  WHY: deduplicate
  HASH: 195b928932b71ffc1192c24eeef6636f0abd40cd
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L267-L269
  DST: docs/dev/guides/frontend-modernization.md#
  WHY: deduplicate
  HASH: 0fa3eeeefcb0c9a309db9dfd8e37ef6bc838d54b
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L385-L387
  DST: docs/dev/guides/frontend-modernization.md#npm-run-build-css
  WHY: deduplicate
  HASH: 58551868785cecfb1cb1c915dc6d58d29de57c9f
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L393-L395
  DST: docs/dev/guides/frontend-modernization.md#npm-install-save-dev-next-bundle-analyzer
  WHY: deduplicate
  HASH: 562b6c6ce389339e063b504c365f999b50a609c0
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L403-L405
  DST: docs/dev/guides/frontend-modernization.md#f-r-entwickler
  WHY: deduplicate
  HASH: ad5136bdc20b8dc1ecc48e24a86c175dcb643857
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L410-L412
  DST: docs/dev/guides/frontend-modernization.md#2-brand-guidelines-farben-typography-spacing
  WHY: deduplicate
  HASH: 4f9cceb1bcd9c5d46dc303cf2d57f11a562ab5df
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L10-L13
  DST: docs/dev/guides/frontend-modernization.md#berblick-der-modernisierung
  WHY: deduplicate
  HASH: 0d4415ba2b32981aa771736225157e7e2cbf3015
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L14-L28
  DST: docs/dev/guides/frontend-modernization.md#dark-mode-support-automatisches-theme-switching-system-sync
  WHY: deduplicate
  HASH: 5eabe4e2fbf8a9ac05f2157a1b9462dd2fa3fb82
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L29-L39
  DST: docs/dev/guides/frontend-modernization.md#
  WHY: deduplicate
  HASH: bf5a40615dd654c1f0170824168ac01b6dd128ef
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L42-L46
  DST: docs/dev/guides/frontend-modernization.md#mkdir-p-src-lib
  WHY: deduplicate
  HASH: f33a8b0257ca90555d9f05fbe0dee66b2f14f226
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L47-L54
  DST: docs/dev/guides/frontend-modernization.md#mkdir-p-src-components-upload
  WHY: deduplicate
  HASH: 296a78cfa20b23a5a199eb71dc97ee5804310fae
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L58-L60
  DST: docs/dev/guides/frontend-modernization.md#
  WHY: deduplicate
  HASH: 5425c4f140d83237ebc1375c874a4efd8ea6efd4
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L61-L63
  DST: docs/dev/guides/frontend-modernization.md#
  WHY: deduplicate
  HASH: 5a86cd972b7e8f2c20081d3493174c2188befcaf
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L64-L67
  DST: docs/dev/guides/frontend-modernization.md#3-error-boundary-src-components-ui-errorboundary-tsx
  WHY: deduplicate
  HASH: cbefba8a2b7e56b2180577c3beb5b7cf7c2d1129
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L71-L76
  DST: docs/dev/guides/frontend-modernization.md#
  WHY: deduplicate
  HASH: 8fc7a67fadc7e74e2bfc01bb52705a776703a5e0
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L77-L84
  DST: docs/dev/guides/frontend-modernization.md#pages-js-ts-jsx-tsx-mdx
  WHY: deduplicate
  HASH: ebf3b64f431efd3f34d4b29c7945818994dbfbcd
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L87-L94
  DST: docs/dev/guides/frontend-modernization.md#fontfamily
  WHY: deduplicate
  HASH: e580343c9ee714c8060b9d90ad7add020ed48cef
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L95-L100
  DST: docs/dev/guides/frontend-modernization.md#
  WHY: deduplicate
  HASH: 85574d19ae71682a4d2a08950963d85ee3dd92e3
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L101-L105
  DST: docs/dev/guides/frontend-modernization.md#import-commandpaletteprovider-from-src-components-ui-commandpalette
  WHY: deduplicate
  HASH: 6a085e15eda05528b40d6b76b95d6fb5d8d2fed7
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L106-L111
  DST: docs/dev/guides/frontend-modernization.md#div-classname-inter-classname
  WHY: deduplicate
  HASH: fc3a43bae0ac7907f966abc5726233c1075a363e
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L112-L118
  DST: docs/dev/guides/frontend-modernization.md#authprovider
  WHY: deduplicate
  HASH: c8dc7a60a9ca9646434dd462464542e7302f0e16
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L119-L123
  DST: docs/dev/guides/frontend-modernization.md#next-public-nlp-api-http-localhost-8003
  WHY: deduplicate
  HASH: 70ad6f3299a2c03b129351d3ac838e91096bfafc
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L205-L214
  DST: docs/dev/guides/frontend-modernization.md#swcminify-true
  WHY: deduplicate
  HASH: 8dcf1b22f0a7c2995fe4e66ea0d2eb8167be6cfa
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L217-L223
  DST: docs/dev/guides/frontend-modernization.md#performance-monitoring
  WHY: deduplicate
  HASH: 982061d8497f86e637aa3b6432e11128f378424a
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L224-L230
  DST: docs/dev/guides/frontend-modernization.md#1-user-experience
  WHY: deduplicate
  HASH: 0cc53d319bba8b917c228d233ba7b71f776e7a38
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L231-L237
  DST: docs/dev/guides/frontend-modernization.md#
  WHY: deduplicate
  HASH: 1ea9534734409e3cd60678b9396e903bd05d17be
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L238-L244
  DST: docs/dev/guides/frontend-modernization.md#
  WHY: deduplicate
  HASH: 8da1c1c09015de892034be59fe93e5da72e19bf5
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L245-L251
  DST: docs/dev/guides/frontend-modernization.md#
  WHY: deduplicate
  HASH: e469aa9fa19327e00ace1bd28dd5ec6a1a11b81f
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L252-L258
  DST: docs/dev/guides/frontend-modernization.md#rm-rf-node-modules-package-lock-json
  WHY: deduplicate
  HASH: 01987c9862394ecafe1022a996e58e9456fb04b6
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L264-L266
  DST: docs/dev/guides/frontend-modernization.md#viewport-meta-tag-pr-fen
  WHY: deduplicate
  HASH: 6dba89c1b53682e8a20bfce4dddcbf59bda028fb
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L270-L272
  DST: docs/dev/guides/frontend-modernization.md#3-api-reference-hook-utility-dokumentation
  WHY: deduplicate
  HASH: c5e9d91df6a624345427cd10855ad09cb380f284
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L276-L279
  DST: docs/dev/guides/frontend-modernization.md#vor-der-modernisierung-baseline
  WHY: deduplicate
  HASH: 569ff08b28ee7e2edfaaa7b144d5761ebf665724
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L280-L293
  DST: docs/dev/guides/frontend-modernization.md#nach-der-modernisierung-ziel
  WHY: deduplicate
  HASH: 024031055d4ce1b84ba711c72ef0c617e41bad16
- ACTION: merge+link
  SRC: docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md#L41-L52
  DST: docs/dev/guides/flowise-agents.md#
  WHY: deduplicate
  HASH: 8c4f2d3edb760f01b03839a92ffa6638a9f0ab96
- ACTION: merge+link
  SRC: docs/dev/v0.2/FlowiseAI-Agents-integration.md#L100-L116
  DST: docs/dev/guides/flowise-agents.md#preset-anbindung-defaults
  WHY: deduplicate
  HASH: d7f926d51d3cfbecfaa9db91875a6a50b31e7058
- ACTION: merge+link
  SRC: docs/dev/v0.2/Preset-Profile.md#L15-L17
  DST: docs/dev/guides/preset-profiles.md#security-runtime
  WHY: deduplicate
  HASH: c825fada8abd4a5cb159329dba891f9739ea0a7b
- ACTION: merge+link
  SRC: docs/dev/v0.2/v0.3+/RAG-Systeme.md#L3-L14
  DST: docs/dev/guides/rag-systems.md#1-zielbild
  WHY: deduplicate
  HASH: aeaf48278f899b1c5a3548f1bf1fcd2b93d22119
- ACTION: merge+link
  SRC: docs/dev/v0.2/v0.3+/RAG-Systeme.md#L17-L22
  DST: docs/dev/guides/rag-systems.md#2-retrieval-relevante-gesetzesparagraphen-unternehmensdaten-politische-akteure
  WHY: deduplicate
  HASH: 29de4a61dd2b4ede69e1b6bfadb89f75ce131980
- ACTION: merge+link
  SRC: docs/dev/v0.2/v0.3+/RAG-Systeme.md#L23-L34
  DST: docs/dev/guides/rag-systems.md#compliance-check-firma-aktivit-t-paragraph
  WHY: deduplicate
  HASH: da622d374e99a16095e32f975833e53cbdcb0d5a
- ACTION: merge+link
  SRC: docs/dev/v0.2/v0.3+/RAG-Systeme.md#L35-L44
  DST: docs/dev/guides/rag-systems.md#
  WHY: deduplicate
  HASH: df5a49c4d18f52cfce17279e41649de372bc0bd7
- ACTION: merge+link
  SRC: docs/dev/v0.2/v0.3+/RAG-Systeme.md#L47-L58
  DST: docs/dev/guides/rag-systems.md#
  WHY: deduplicate
  HASH: 5d47284b638038db947fc6a90d04f2037b87af8c
- ACTION: merge+link
  SRC: docs/dev/v0.2/v0.3+/RAG-Systeme.md#L59-L72
  DST: docs/dev/guides/rag-systems.md#
  WHY: deduplicate
  HASH: a97122c610a158a3a23b39b581c662f3fb8f0afe
- ACTION: merge+link
  SRC: docs/dev/v0.2/Preset-Profile.md#L1-L8
  DST: docs/dev/guides/preset-profiles.md#presets-profile-berblick
  WHY: deduplicate
  HASH: f69754c2e1d3506ea43396ac9bc67e489bcf6bf3
- ACTION: merge+link
  SRC: docs/presets/Presets(Profile).md#L1-L8
  DST: docs/dev/guides/preset-profiles.md#presets-profile-berblick
  WHY: deduplicate
  HASH: 0f9e421c6c4158543442150b65a71366efab4fdb
- ACTION: merge+link
  SRC: docs/dev/v0.2/Preset-Profile.md#L11-L14
  DST: docs/dev/guides/preset-profiles.md#it-egress-tor-vpn
  WHY: deduplicate
  HASH: aa8d02d4479c54f931913f4a08271b6e90b02c01
- ACTION: merge+link
  SRC: docs/presets/Presets(Profile).md#L11-L14
  DST: docs/dev/guides/preset-profiles.md#betriebsmodus
  WHY: deduplicate
  HASH: 22c20b41d50061194a524e21b6bfb6b4e5736a20
- ACTION: merge+link
  SRC: docs/presets/Presets(Profile).md#L15-L17
  DST: docs/dev/guides/preset-profiles.md#it-no-log-persist-1
  WHY: deduplicate
  HASH: 56aae59d9fa77be82dc5c71e3d2b248f0dff2036
- ACTION: merge+link
  SRC: docs/dev/v0.2/Preset-Profile.md#L18-L27
  DST: docs/dev/guides/preset-profiles.md#it-browser-profile-strict
  WHY: deduplicate
  HASH: d715bbd245e0ef20ef30d3d635b36d23d9a5b90f
- ACTION: merge+link
  SRC: docs/presets/Presets(Profile).md#L18-L27
  DST: docs/dev/guides/preset-profiles.md#it-browser-profile-strict
  WHY: deduplicate
  HASH: 947bff06481e9b2da98f8d167ad42cf12f38fc60
- ACTION: merge+link
  SRC: docs/dev/v0.2/Preset-Profile.md#L28-L35
  DST: docs/dev/guides/preset-profiles.md#robots-enforce-true
  WHY: deduplicate
  HASH: df6e1d1351a903f5180b5539f0418a7b88522015
- ACTION: merge+link
  SRC: docs/presets/Presets(Profile).md#L28-L35
  DST: docs/dev/guides/preset-profiles.md#robots-enforce-true
  WHY: deduplicate
  HASH: df6e1d1351a903f5180b5539f0418a7b88522015
- ACTION: merge+link
  SRC: docs/dev/v0.2/Preset-Profile.md#L36-L42
  DST: docs/dev/guides/preset-profiles.md#verif
  WHY: deduplicate
  HASH: 30c6fb16b6a9682b4600eb3c281cce0a2c7fbc3f
- ACTION: merge+link
  SRC: docs/presets/Presets(Profile).md#L36-L42
  DST: docs/dev/guides/preset-profiles.md#verif
  WHY: deduplicate
  HASH: 5e66c6381fd70d269db39232abea479772dba5dc
- ACTION: merge+link
  SRC: docs/dev/v0.2/Preset-Profile.md#L55-L60
  DST: docs/dev/guides/preset-profiles.md#2-beh-rden-firmen-preset-forensics
  WHY: deduplicate
  HASH: 71603745d01dab4816a18a23929a2a9c93c13f68
- ACTION: merge+link
  SRC: docs/presets/Presets(Profile).md#L55-L60
  DST: docs/dev/guides/preset-profiles.md#review-ui-review-before-share-erzwungen
  WHY: deduplicate
  HASH: 98a943d82d03c06a4c16a63ed37d517a2f01a5e9
- ACTION: merge+link
  SRC: docs/dev/v0.2/Preset-Profile.md#L75-L81
  DST: docs/dev/guides/preset-profiles.md#provenienz-hash
  WHY: deduplicate
  HASH: 81e10f4a33a043ee2882a5446d95e6251553a64d
- ACTION: merge+link
  SRC: docs/presets/Presets(Profile).md#L84-L90
  DST: docs/dev/guides/preset-profiles.md#provenienz-hash
  WHY: deduplicate
  HASH: 38a58bae6d434270e1cbb80d5684cf6155cb5cd2
- ACTION: merge+link
  SRC: docs/dev/v0.2/Preset-Profile.md#L82-L88
  DST: docs/dev/guides/preset-profiles.md#yaml
  WHY: deduplicate
  HASH: 51d95ccabcff5ed626f160a61029301b99bd3823
- ACTION: merge+link
  SRC: docs/presets/Presets(Profile).md#L91-L97
  DST: docs/dev/guides/preset-profiles.md#yaml
  WHY: deduplicate
  HASH: e7919a4a0fe80fbd68ea519a80c039465324a925
- ACTION: merge+link
  SRC: docs/dev/v0.2/Preset-Profile.md#L91-L94
  DST: docs/dev/guides/preset-profiles.md#graphx-timeline-geo-standardm-ig-an-evidence-per-edge-sichtbar
  WHY: deduplicate
  HASH: 1fc0ab24b3571aa58bfb12b40a0cfcf9254b467f
- ACTION: merge+link
  SRC: docs/presets/Presets(Profile).md#L100-L103
  DST: docs/dev/guides/preset-profiles.md#evidence-required
  WHY: deduplicate
  HASH: 1670a44334e6074b3e5fee6e2c8648807a9ad391
- ACTION: merge+link
  SRC: docs/dev/v0.2/Preset-Profile.md#L106-L113
  DST: docs/dev/guides/preset-profiles.md#
  WHY: deduplicate
  HASH: 30b530246aacbaf9f66e50dceb1ebdc8b79af519
- ACTION: merge+link
  SRC: docs/presets/Presets(Profile).md#L115-L122
  DST: docs/dev/guides/preset-profiles.md#
  WHY: deduplicate
  HASH: 2e95b84f600586ade85456256125e63035355e3b
- ACTION: merge+link
  SRC: docs/dev/v0.2/Preset-Profile.md#L114-L118
  DST: docs/dev/guides/preset-profiles.md#geo-enrich-standard-cache-aggressiver
  WHY: deduplicate
  HASH: 0ac201b1387cf89eb158b77bdf9194b8765c1f3a
- ACTION: merge+link
  SRC: docs/presets/Presets(Profile).md#L123-L127
  DST: docs/dev/guides/preset-profiles.md#it-doh-1
  WHY: deduplicate
  HASH: 73e4ef4827f2c870a91b7e09ea9c70810503cf60
- ACTION: merge+link
  SRC: docs/dev/v0.2/Preset-Profile.md#L119-L124
  DST: docs/dev/guides/preset-profiles.md#
  WHY: deduplicate
  HASH: f0db3671a7b833e93ec2c56f6797d8caffa95050
- ACTION: merge+link
  SRC: docs/presets/Presets(Profile).md#L128-L133
  DST: docs/dev/guides/preset-profiles.md#geo-enrich-standard-cache-aggressiver
  WHY: deduplicate
  HASH: a9af9795b39b19f49bc5f41c79cf8e6074c27c0c
- ACTION: merge+link
  SRC: docs/dev/v0.2/Preset-Profile.md#L139-L145
  DST: docs/dev/guides/preset-profiles.md#review-ui-override-erlaubt-label-store-prominent
  WHY: deduplicate
  HASH: 320c6bb0f054816c880531ae5c2e31079c6c43e9
- ACTION: merge+link
  SRC: docs/presets/Presets(Profile).md#L157-L163
  DST: docs/dev/guides/preset-profiles.md#active-learning-true
  WHY: deduplicate
  HASH: af17030a44b335945f4960d2e5da084f0a1125f1
- ACTION: merge+link
  SRC: docs/dev/v0.2/Preset-Profile.md#L146-L152
  DST: docs/dev/guides/preset-profiles.md#it-profile-journalism-agency-research
  WHY: deduplicate
  HASH: 1b5a113651d190dfb7b99094aed218aab9c5f953
- ACTION: merge+link
  SRC: docs/presets/Presets(Profile).md#L164-L170
  DST: docs/dev/guides/preset-profiles.md#allowed-alle-passiven-forensischen-tools-aktive-nur-im-lab-isolated-netz-preset-pr-ft-sandbox-no-net
  WHY: deduplicate
  HASH: ea2938a2ad7902fc64134193eb16242c7978ab14
- ACTION: merge+link
  SRC: docs/dev/v0.2/Preset-Profile.md#L155-L158
  DST: docs/dev/guides/preset-profiles.md#egress-tor-vpn
  WHY: deduplicate
  HASH: c8e963fad3f8a005d1b7a0dd27d3cde7c9c30015
- ACTION: merge+link
  SRC: docs/presets/Presets(Profile).md#L173-L176
  DST: docs/dev/guides/preset-profiles.md#security-env-proxy-wiring
  WHY: deduplicate
  HASH: b0094d951ae9cd8ae69a5f28f12c7fc87a8154de
- ACTION: merge+link
  SRC: docs/dev/v0.2/Preset-Profile.md#L170-L176
  DST: docs/dev/guides/preset-profiles.md#
  WHY: deduplicate
  HASH: b01d0b6da0a3b43ee3ed9e1e27296272f55e653e
- ACTION: merge+link
  SRC: docs/presets/Presets(Profile).md#L188-L194
  DST: docs/dev/guides/preset-profiles.md#search-defaults-badges-min-likely-true-time-range-72h
  WHY: deduplicate
  HASH: c0892fa2e0c113bc2dc1a95dd167ec3bb9b26edc
- ACTION: merge+link
  SRC: docs/dev/v0.2/Preset-Profile.md#L186-L191
  DST: docs/dev/guides/preset-profiles.md#
  WHY: deduplicate
  HASH: ebffffc7419abf04f08931bdb2507b82ac984660
- ACTION: merge+link
  SRC: docs/presets/Presets(Profile).md#L204-L209
  DST: docs/dev/guides/preset-profiles.md#forschung
  WHY: deduplicate
  HASH: 5729ee441ec52adad5b2ffc088eaa5c5fe892b8b
- ACTION: merge+link
  SRC: docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md#L142-L143
  DST: docs/dev/guides/flowise-agents.md#docs-nodes-flowise-n8n-md
  WHY: deduplicate
  HASH: d82fb76eda356eab5f1f4fa1210bfafc837b92e1
- ACTION: merge+link
  SRC: docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md#L190-L191
  DST: docs/dev/guides/flowise-agents.md#markdown
  WHY: deduplicate
  HASH: 9a26f77641edb927ebfe85ca9d883f325f7bcbc8
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L114-L116
  DST: docs/dev/guides/frontend-modernization.md#environment-variables
  WHY: deduplicate
  HASH: 8c145c396b9875b9020099c8ca948d6dea8db3cc
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L167-L169
  DST: docs/dev/guides/frontend-modernization.md#bash
  WHY: deduplicate
  HASH: c6498274dcd242bc4fc11f0262ba77735f20caca
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L32-L34
  DST: docs/dev/guides/frontend-modernization.md#optional-advanced-components
  WHY: deduplicate
  HASH: 1fe832aaaa713282808063059ffa10a2e5cc085d
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L35-L38
  DST: docs/dev/guides/frontend-modernization.md#section
  WHY: deduplicate
  HASH: 51dff0d72a3c17aac4d68f6b697eaa0bb1d00fbf
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L123-L129
  DST: docs/dev/guides/frontend-modernization.md#phase-2-navigation-layout-tag-3-4
  WHY: deduplicate
  HASH: 4f0d9056d18dd05c47e380a0f197ed90dc66165a
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L130-L136
  DST: docs/dev/guides/frontend-modernization.md#section
  WHY: deduplicate
  HASH: c747624fda9251d3685dfb37d3087caa1762a56b
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L137-L143
  DST: docs/dev/guides/frontend-modernization.md#graph-viewer-erweitern
  WHY: deduplicate
  HASH: eb4ce225cfa0f9af3d5cc1fd1e1c6f48593d6c61
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L151-L157
  DST: docs/dev/guides/frontend-modernization.md#npm-run-e2e
  WHY: deduplicate
  HASH: a27d47a2138c3e87c16ce5bda7ca7c84ee21a49e
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L158-L164
  DST: docs/dev/guides/frontend-modernization.md#notifications-toast-messages
  WHY: deduplicate
  HASH: 50712228e48b767cfb264678b5e9f18feb07c4c5
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L248-L250
  DST: docs/dev/guides/frontend-modernization.md#section
  WHY: deduplicate
  HASH: bfff20d48757c4e1a4dcc8416d729cd1a9c97b69
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L174-L176
  DST: docs/dev/guides/frontend-modernization.md#first-input-delay-100ms
  WHY: deduplicate
  HASH: e1d69a33b8bd0cc601cbd5466dc180ab6137b022
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L182-L195
  DST: docs/dev/guides/frontend-modernization.md#section
  WHY: deduplicate
  HASH: ca9b116d2b6b722b4e51a0cf5e704f2c63e5efc6
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L207-L214
  DST: docs/dev/guides/frontend-modernization.md#4-mobile-issues
  WHY: deduplicate
  HASH: 4c5b8f6c0ecb4d0779041023b417bf5dae061e13
- ACTION: merge+link
  SRC: docs/dev/v0.2/v0.3+/RAG-Systeme.md#L6-L11
  DST: docs/dev/guides/rag-systems.md#a-rag-speicher
  WHY: deduplicate
  HASH: d6b886335d31ab4b5578d6c4ab9bcbe355d467ce
- ACTION: merge+link
  SRC: docs/dev/v0.2/Preset-Profile.md#L67-L79
  DST: docs/dev/guides/preset-profiles.md#nifi-pipelines-aktiviert
  WHY: deduplicate
  HASH: 0e435cba08de6bf71f7feefff7beacee75a40931
- ACTION: merge+link
  SRC: docs/presets/Presets(Profile).md#L76-L88
  DST: docs/dev/guides/preset-profiles.md#nifi-pipelines-aktiviert
  WHY: deduplicate
  HASH: d2b92da2964ba49d975be1bd2168670da81f927a
- ACTION: merge+link
  SRC: docs/dev/v0.2/Preset-Profile.md#L92-L98
  DST: docs/dev/guides/preset-profiles.md#section
  WHY: deduplicate
  HASH: 062ac3a5c40b5ff9efa7e003ea7749c754ed78ef
- ACTION: merge+link
  SRC: docs/presets/Presets(Profile).md#L110-L115
  DST: docs/dev/guides/preset-profiles.md#it-ephemeral-fs-0
  WHY: deduplicate
  HASH: cadb0fc9db7042602eae7dc186546555451d92c7
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L202-L204
  DST: docs/dev/guides/frontend-modernization.md#3-performance-issues
  WHY: deduplicate
  HASH: de2ef984055c3d4d003fd4caacf46c7dd325171f
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L194-L196
  DST: docs/dev/guides/frontend-modernization.md#typescript-errors
  WHY: deduplicate
  HASH: 484ed9202cdc4da6a5541ae49222ee57bc5b1e4e
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L147-L149
  DST: docs/dev/guides/frontend-modernization.md#unit-tests
  WHY: deduplicate
  HASH: 890a866fd9055326c57ca2762079608e7d3f00c5
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L227-L230
  DST: docs/dev/guides/frontend-modernization.md#10x-bessere-user-experience
  WHY: deduplicate
  HASH: 13abbcffc0a3c86357da64246e4e2d7742d6168e
- ACTION: merge+link
  SRC: docs/presets/Presets(Profile).md#L50-L58
  DST: docs/dev/guides/preset-profiles.md#frontend-defaults
  WHY: deduplicate
  HASH: 46b2929bc635fe47816acd49a9f1b061b472e58f
- ACTION: merge+link
  SRC: docs/dev/v0.2/Preset-Profile.md#L41-L47
  DST: docs/dev/guides/preset-profiles.md#frontend-defaults
  WHY: deduplicate
  HASH: 9ea2ffa4469665ad1d678b10a3edc74f95df80c4
- ACTION: merge+link
  SRC: docs/presets/Presets(Profile).md#L98-L103
  DST: docs/dev/guides/preset-profiles.md#bash
  WHY: deduplicate
  HASH: 7e328af6f7dc9f9fcf5ba270be410113f1c02340
- ACTION: merge+link
  SRC: docs/dev/v0.2/Preset-Profile.md#L80-L86
  DST: docs/dev/guides/preset-profiles.md#section
  WHY: deduplicate
  HASH: f1d212e26d83fd8cdd0a462b46543bb598bfe5cb
- ACTION: merge+link
  SRC: docs/dev/guides/frontend-modernization-setup-guide.md#L221-L224
  DST: docs/dev/guides/frontend-modernization.md#herzlichen-gl-ckwunsch
  WHY: deduplicate
  HASH: dd636f623e3bdec7316c690c0ca2e60452e48785
- ACTION: merge+link
  SRC: docs/export/AFFINE.md#L1-L2
  DST: docs/dev/guides/flowise-agents.md#docs-export-affine-md
  WHY: deduplicate
  HASH: 659610de45e3692cf1bd95c6bbf2aa37c6b4410d
- ACTION: merge+link
  SRC: docs/export/AFFINE.md#L105-L106
  DST: docs/dev/guides/flowise-agents.md#docs-export-bundle-spec-md
  WHY: deduplicate
  HASH: 20ff2ae62c1699f750aaaafd7b947e8d8df6cea7
- ACTION: merge+link
  SRC: docs/waveterm/README.md#L8-L10
  DST: docs/dev/guides/flowise-agents.md#docs-waveterm-readme-md
  WHY: deduplicate
  HASH: ca2385a1125dbfc15552f42c96d9ac12f54bb5b2
- ACTION: merge+link
  SRC: docs/waveterm/README.md#L229-L231
  DST: docs/dev/guides/flowise-agents.md#markdown
  WHY: deduplicate
  HASH: ab73d1113ca30d5a948c8f1f38e65cc3faf9402c
- ACTION: merge+link
  SRC: docs/waveterm/README.md#L335-L337
  DST: docs/dev/guides/flowise-agents.md#section
  WHY: deduplicate
  HASH: e35919f68683daa3038cc855ee48846ebc9ae4d7
- ACTION: merge+link
  SRC: docs/waveterm/README.md#L366-L367
  DST: docs/dev/guides/flowise-agents.md#command-string-template
  WHY: deduplicate
  HASH: 3307b76cf28b7829b207942c3ccd45679154476d
- ACTION: merge+link
  SRC: docs/export/APPFLOWY.md#L2-L4
  DST: docs/dev/guides/flowise-agents.md#docs-export-appflowy-md
  WHY: deduplicate
  HASH: 151bd73ed4c7fa42cfca80cd268791e7d5e74e6a
- ACTION: merge+link
  SRC: docs/waveterm/README.md#L331-L333
  DST: docs/dev/guides/flowise-agents.md#docs-n8n-waveterm-run-md
  WHY: deduplicate
  HASH: 54982470270be37c705c5bd06b30cd9fadd9f527
- ACTION: merge+link
  SRC: docs/waveterm/README.md#L360-L361
  DST: docs/dev/guides/flowise-agents.md#nifi-processor-waveterminvoker
  WHY: deduplicate
  HASH: 764fa53e1f4100988f1c39b46a12c4ef76ee1670
- ACTION: merge+link
  SRC: docs/dev/nifi-aleph.md#L11-L13
  DST: docs/dev/guides/frontend-modernization.md#setup
  WHY: deduplicate
  HASH: 3b774861b0350b97e2f23a216cb1c2f3efafb643

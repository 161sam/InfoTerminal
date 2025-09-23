import type { Entity as BaseEntity } from "@/lib/nlp";

export type Entity = BaseEntity & {
  value?: string;
  node_id?: string;
  resolution_status?: string;
  resolution_score?: number;
  resolution_target?: string;
};

export type DocMeta = {
  title?: string;
  source?: string;
  aleph_id?: string;
  created_at?: string;
  linking_status_counts?: Record<string, number>;
  linking_mean_score?: number;
  linking_resolved?: number;
  linking_unmatched?: number;
  linking_pending?: number;
};

export type DocRecord = {
  id: string;
  doc_id?: string;
  text?: string;
  entities: Entity[];
  relations?: any[];
  meta?: DocMeta;
  metadata?: DocMeta;
  html_content?: string | null;
};

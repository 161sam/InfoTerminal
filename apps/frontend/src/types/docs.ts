import type { Entity as BaseEntity } from "@/lib/nlp";

export type Entity = BaseEntity & {
  node_id?: string;
};

export type DocMeta = {
  title?: string;
  source?: string;
  aleph_id?: string;
  created_at?: string;
};

export type DocRecord = {
  id: string;
  text: string;
  entities: Entity[];
  meta?: DocMeta;
};

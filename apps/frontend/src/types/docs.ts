export type Entity = {
  start: number;
  end: number;
  label: string;
  text?: string;
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

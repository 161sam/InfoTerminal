interface Props {
  sort: string;
  onSortChange: (sort: string) => void;
  rerank: boolean;
  onRerankToggle: (v: boolean) => void;
}

export default function SortAndRerank({ sort, onSortChange, rerank, onRerankToggle }: Props) {
  return (
    <div>
      <select value={sort} onChange={(e) => onSortChange(e.target.value)}>
        <option value="relevance">relevance</option>
        <option value="date_desc">newest</option>
        <option value="date_asc">oldest</option>
      </select>
      <label>
        <input
          type="checkbox"
          checked={rerank}
          onChange={(e) => onRerankToggle(e.target.checked)}
        />
        Rerank
      </label>
    </div>
  );
}

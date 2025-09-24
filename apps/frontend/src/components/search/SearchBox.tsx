import { useEffect, useState } from "react";

interface Props {
  value?: string;
  onChange?: (value: string) => void;
  onSubmit?: (value: string) => void;
  loading?: boolean;
}

export default function SearchBox({ value = "", onChange, onSubmit, loading }: Props) {
  const [term, setTerm] = useState(value);

  useEffect(() => {
    setTerm(value);
  }, [value]);

  useEffect(() => {
    const t = setTimeout(() => {
      onChange?.(term);
    }, 300);
    return () => clearTimeout(t);
  }, [term, onChange]);

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        onSubmit?.(term);
      }}
    >
      <input placeholder="Search..." value={term} onChange={(e) => setTerm(e.target.value)} />
      <button type="submit" disabled={loading}>
        {loading ? "..." : "Search"}
      </button>
      {term && (
        <button type="button" onClick={() => setTerm("")}>
          ×
        </button>
      )}
    </form>
  );
}

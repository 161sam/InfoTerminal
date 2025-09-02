import { useState, FormEvent } from 'react';

export default function SearchBox({ onSubmit }: { onSubmit: (q: string) => void }) {
  const [value, setValue] = useState('');
  const submit = (e: FormEvent) => {
    e.preventDefault();
    onSubmit(value);
  };
  return (
    <form onSubmit={submit}>
      <input
        placeholder="Search"
        value={value}
        onChange={e => setValue(e.target.value)}
      />
      <button type="submit">Search</button>
    </form>
  );
}

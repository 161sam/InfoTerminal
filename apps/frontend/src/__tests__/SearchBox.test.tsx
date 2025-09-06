import { render, screen, fireEvent } from '@testing-library/react';
import SearchBox from '@/components/search/SearchBox';

it('renders and triggers onSubmit', async () => {
  const onSubmit = vi.fn();
  render(<SearchBox onSubmit={onSubmit} />);
  const input = screen.getByPlaceholderText(/search/i);
  await fireEvent.input(input, { target: { value: 'neo4j' } });
  const btn = screen.getByRole('button', { name: /search/i });
  await fireEvent.click(btn);
  expect(onSubmit).toHaveBeenCalledWith('neo4j');
});

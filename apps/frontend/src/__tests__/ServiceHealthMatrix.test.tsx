import { render, screen, fireEvent } from '@testing-library/react';
import ServiceHealthMatrix from '@/components/ServiceHealthMatrix';

vi.mock('@/hooks/useServiceHealthMatrix', () => ({
  __esModule: true,
  default: () => ({ search: { status: 'ok', latency: 1 } }),
}));

test('renders badges and toggles details', () => {
  render(<ServiceHealthMatrix />);
  const wrapper = screen.getByTestId('svc-health');
  expect(wrapper.querySelectorAll('span').length).toBe(1);
  const btn = wrapper.querySelector('button')!;
  fireEvent.click(btn);
  expect(screen.getByText('search')).toBeInTheDocument();
});

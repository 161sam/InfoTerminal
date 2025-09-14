import { render, screen } from '@testing-library/react';
import Renderer from '../components/nlp/Renderer';

test('renders provided HTML', () => {
  render(<Renderer html="<span>hi</span>" />);
  expect(screen.getByText('hi')).toBeInTheDocument();
});

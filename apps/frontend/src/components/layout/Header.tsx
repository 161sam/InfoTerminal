import React from 'react';
import GlobalHealth from '../health/GlobalHealth';

const Header: React.FC = () => (
  <header className="flex items-center justify-between px-4 py-2 shadow-md">
    <a href="/" className="font-bold">InfoTerminal</a>
    <nav className="flex gap-4">
      <a href="/demo">Demo</a>
    </nav>
    <GlobalHealth />
  </header>
);

export default Header;

import React from 'react';
import { NavLink } from 'react-router-dom';

const Sidebar: React.FC = () => {
  const links = [
    { name: 'Dashboard', path: '/' },
    { name: 'Upload Resume', path: '/upload' },
    { name: 'Career Insights', path: '/insights' },
    { name: 'Profile', path: '/profile' },
  ];

  return (
    <aside className="w-64 min-h-screen bg-white border-r border-gray-200 p-4">
      <nav className="space-y-2">
        {links.map((link) => (
          <NavLink
            key={link.path}
            to={link.path}
            className={({ isActive }) =>
              `block px-4 py-3 rounded-lg transition ${
                isActive
                  ? 'bg-indigo-100 text-indigo-700 font-semibold'
                  : 'text-gray-600 hover:bg-gray-100'
              }`
            }
          >
            {link.name}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
};

export default Sidebar;
import React from 'react';

const Sidebar = () => {
  return (
    <aside className="sidebar">
      <nav>
        <ul className="sidebar-nav">
          <li>
            <a href="#" className="active">Dashboard</a>
          </li>
          <li>
            <a href="#">About</a>
          </li>
          <li>
            <a href="#">Help</a>
          </li>
        </ul>
      </nav>
    </aside>
  );
};

export default Sidebar;
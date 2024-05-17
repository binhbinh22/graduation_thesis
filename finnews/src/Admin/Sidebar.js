import React from 'react';

const Sidebar = () => {
  return (
    <aside className="admin-sidebar">
      <ul>
        <li><a href="/admin/posts">Quản lý bài viết</a></li>
        {/* Thêm các mục điều hướng khác tại đây */}
      </ul>
    </aside>
  );
};

export default Sidebar;

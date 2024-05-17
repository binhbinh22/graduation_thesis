import React from 'react';

const PostList = ({ posts }) => {
  return (
    <div className="post-list">
      <h2>Danh sách bài viết</h2>
      <ul>
        {posts.map(post => (
          <li key={post.id}>
            <h3>{post.title}</h3>
            <p>{post.summary}</p>
            <button>Xoá</button>
            {/* Thêm nút sửa và xem chi tiết bài viết */}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default PostList;

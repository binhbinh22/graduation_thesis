import React, { useState } from 'react';
import Header from './Header';
import Sidebar from './Sidebar';
import PostList from './PostList';
import AddPostForm from './AddPostForm';

const AdminPage = () => {
  const [posts, setPosts] = useState([]);

  const handleAddPost = (newPost) => {
    setPosts([...posts, { id: Date.now(), ...newPost }]);
  };

  return (
    <div className="admin-page">
      <Header />
      <div className="admin-content">
        <Sidebar />
        <main>
          <AddPostForm onAdd={handleAddPost} />
          <PostList posts={posts} />
        </main>
      </div>
    </div>
  );
};

export default AdminPage;

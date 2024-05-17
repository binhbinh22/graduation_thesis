import React, { useState } from 'react';

const AddPostForm = ({ onAdd }) => {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onAdd({ title, content });
    setTitle('');
    setContent('');
  };

  return (
    <div className="add-post-form">
      <h2>Thêm mới bài viết</h2>
      <form onSubmit={handleSubmit}>
        <input type="text" placeholder="Tiêu đề" value={title} onChange={(e) => setTitle(e.target.value)} />
        <textarea placeholder="Nội dung" value={content} onChange={(e) => setContent(e.target.value)}></textarea>
        <button type="submit">Thêm</button>
      </form>
    </div>
  );
};

export default AddPostForm;

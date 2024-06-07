import React, { useState, useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../Contexts/AuthContext';

const SelectTag = () => {
  const [tags, setTags] = useState([]);
  const [selectedTags, setSelectedTags] = useState([]);
  const { user } = useContext(AuthContext);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchTags = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/tags/');
        if (!response.ok) {
          throw new Error('Failed to fetch tags');
        }
        const data = await response.json();
        setTags(data);
      } catch (error) {
        console.error('Error fetching tags:', error);
      }
    };

    fetchTags();
  }, []);

  const handleTagClick = (tagId) => {
    setSelectedTags((prevSelectedTags) => {
      if (prevSelectedTags.includes(tagId)) {
        return prevSelectedTags.filter((id) => id !== tagId);
      } else {
        return [...prevSelectedTags, tagId];
      }
    });
  };

  const handleSave = async () => {
    try {
      const responses = await Promise.all(
        selectedTags.map(async (tagId) => {
          const payload = {
            user: user.id,
            tag: tagId,
          };
          
          const response = await fetch('http://127.0.0.1:8000/api/user-tags/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
          });
          console.log('Payload to be sent:', JSON.stringify(payload));
          if (!response.ok) {
            const data = await response.json();
            throw new Error(data.message);
          }
          return response;
        })
      );
      navigate('/news');
    } catch (error) {
      console.error('Error saving user tags:', error);
    }
  };

  return (
    <div className="select-tag-container">
      <h2>Chọn các chủ đề bạn quan tâm</h2>
      <p> Lựa chọn ít nhất 3 chủ đề </p>
      <div className="tag-list">
        {tags.map((tag) => (
          <button
            key={tag.id}
            className={selectedTags.includes(tag.id) ? 'tag-button selected' : 'tag-button'}
            onClick={() => handleTagClick(tag.id)}
          >
            {tag.name}
          </button>
        ))}
      </div>
      <button onClick={handleSave} className="save-button">Lưu</button>
    </div>
  );
};

export default SelectTag;




import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const SelectTags = () => {
  const [tags, setTags] = useState([]);
  const [selectedTags, setSelectedTags] = useState([]);
  const navigate = useNavigate();

  // Function to handle tag selection
  const toggleTag = (tagId) => {
    if (selectedTags.includes(tagId)) {
      setSelectedTags(selectedTags.filter(id => id !== tagId));
    } else {
      setSelectedTags([...selectedTags, tagId]);
    }
  };

  // Function to handle saving selected tags
  const saveTags = async () => {
    // Perform save operation (e.g., send selectedTags to backend)
    console.log('Selected tags:', selectedTags);
    // After saving, navigate to News page
    navigate('/news');
  };

  // Fetch tags from backend on component mount
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

  return (
    <div className="select-tags-container">
      <h2>Chọn các tags bạn quan tâm</h2>
      <div className="tags-list">
        {tags.map(tag => (
          <div key={tag.id} className={`tag-item ${selectedTags.includes(tag.id) ? 'selected' : ''}`} onClick={() => toggleTag(tag.id)}>
            {tag.name}
          </div>
        ))}
      </div>
      <button onClick={saveTags}>Lưu</button>
    </div>
  );
};

export default SelectTags;

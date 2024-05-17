import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import './NewsDetail.css'; // Import CSS

const NewsDetail = () => {
  const { id } = useParams();
  const [newsItem, setNewsItem] = useState(null);
  const [highlightedContent, setHighlightedContent] = useState('');

  useEffect(() => {
    const fetchNewsItem = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/guest/news/${id}/`);
        if (!response.ok) {
          throw new Error('Failed to fetch news item');
        }
        const data = await response.json();
        setNewsItem(data);
      } catch (error) {
        console.error('Error fetching news item:', error);
      }
    };

    fetchNewsItem();
  }, [id]);

  const handleHighlight = () => {
    const importantKeywords = [
      /(hiệp định|thông tư|thuế|quy định|cấm|xuất khẩu|nhập khẩu)/gi,
      /(chiến tranh)/gi,
      /(khí hậu|biến đổi|hiệu ứng|độ ẩm|nhiệt độ|mưa|lụt|hạn hán|nóng|lạnh)/gi,
      /(kinh tế thế giới|dự trữ|khan hiếm|giao dịch|lạm phát)/gi,
      /(dịch bệnh)/gi,
      /(Nhà nước)/gi,
      /(thời tiết)/gi, // Thêm từ khóa cần highlight vào đây
    ];

    let content = newsItem.content;
    const sentences = content.split('. ');

    sentences.forEach((sentence) => {
      importantKeywords.forEach((keyword) => {
        if (keyword.test(sentence)) {
          content = content.replace(
            sentence,
            `<span class="highlight">${sentence}</span>`
          );
        }
      });
    });

    setHighlightedContent(content);
  };

  if (!newsItem) {
    return <div>Loading...</div>;
  }

  return (
    <div className="news-detail">
    <div>
      <button className="highlight-btn" onClick={handleHighlight}>
        Nguyên Nhân
      </button>
    </div>
      <p>{newsItem.topic}</p>
      <h2>{newsItem.title}</h2>
      <p>{newsItem.time}</p>
      <p
        className="content"
        dangerouslySetInnerHTML={{ __html: highlightedContent || newsItem.content }}
      ></p>
      <p>{newsItem.author}</p>
    </div>
  );
};

export default NewsDetail;

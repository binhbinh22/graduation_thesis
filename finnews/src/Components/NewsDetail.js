import React, { useState, useEffect, useContext } from 'react';
import { useParams } from 'react-router-dom';
import { AuthContext } from '../Contexts/AuthContext';
import InfoExtractModal from './InfoExtractModal';
import saveIcon from './icons/bookmark.png'; // Path to your save icon image
import infoIcon from './icons/info.png'; // Path to your info icon image
// import starIcon from './icons/star.png'; // Path to your star icon image
import './NewsDetail.css'; // Assuming you have a separate CSS file for styling

const NewsDetail = () => {
  const { id } = useParams();
  const [newsItem, setNewsItem] = useState(null);
  const [highlightedContent, setHighlightedContent] = useState('');
  const [isSaved, setIsSaved] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const { user } = useContext(AuthContext);

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
      /(thời tiết)/gi,
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

  const handleSave = async () => {
    if (!user || !newsItem) {
      console.error('User or news item is not available');
      return;
    }

    const saveData = {
      user: user.id,
      news: newsItem.id,
    };

    try {
      const response = await fetch('http://127.0.0.1:8000/api/save_news/', {
        method: isSaved ? 'DELETE' : 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(saveData),
      });

      if (!response.ok) {
        throw new Error(`Failed to ${isSaved ? 'unsave' : 'save'} news item`);
      }

      setIsSaved(!isSaved);
    } catch (error) {
      console.error(`Error ${isSaved ? 'unsaving' : 'saving'} news item:`, error);
    }
  };

  const toggleModal = () => {
    setShowModal(!showModal);
  };

  if (!newsItem) {
    return <div>Loading...</div>;
  }

  return (
    <div className="news-detail-container">
      <div className="news-detail-sidebar">
        <div className="tooltip">
    <button className="action-btn" onClick={handleSave}>
      <img src={saveIcon} alt="Save" /> {isSaved ? 'Đã Lưu' : ''}
    </button>
    <span className="tooltiptext">Thêm vào tin tức yêu thích</span>
  </div>
        <div className="tooltip">
          <button className="action-btn" onClick={toggleModal}>
          <img src={infoIcon} alt="Info" /> 
          </button>
          <span className="tooltiptext">Xem thông tin quan trọng</span>
        </div>
        {/* <div className="tooltip">
          <button className="action-btn" onClick={handleHighlight}>
          <img src={starIcon} alt="Highlight" />
          </button>
          <span className="tooltiptext">Điểm đáng lưu ý</span>
        </div> */}

        {/* <button className="action-btn" onClick={toggleModal}>
          <img src={infoIcon} alt="Info" /> 
        </button>
        <button className="action-btn" onClick={handleHighlight}>
          <img src={starIcon} alt="Highlight" />
        </button> */}
      </div>

      <div className="news-detail-content">
        <p>{newsItem.topic}</p>
        <h2 style={{ marginTop: '0px', marginBottom: '0px' }}>{newsItem.title}</h2>
        <p>{newsItem.time}</p>
        <p
          className="content"
          dangerouslySetInnerHTML={{ __html: highlightedContent || newsItem.content }}
        ></p>
        <p>{newsItem.author}</p>
      </div>

      <InfoExtractModal 
        isOpen={showModal} 
        onClose={toggleModal} 
        content={newsItem.info_extrac} 
      />
    </div>
  );
};

export default NewsDetail;




// import React, { useState, useEffect, useContext } from 'react';
// import { useParams } from 'react-router-dom';
// import { AuthContext } from '../Contexts/AuthContext';
// const NewsDetail = () => {
//   const { id } = useParams();
//   const [newsItem, setNewsItem] = useState(null);
//   const [highlightedContent, setHighlightedContent] = useState('');
//   const [isSaved, setIsSaved] = useState(false);
//   const { user } = useContext(AuthContext);
//   useEffect(() => {
//     const fetchNewsItem = async () => {
//       try {
//         const response = await fetch(`http://127.0.0.1:8000/api/guest/news/${id}/`);
//         if (!response.ok) {
//           throw new Error('Failed to fetch news item');
//         }
//         const data = await response.json();
//         setNewsItem(data);
//       } catch (error) {
//         console.error('Error fetching news item:', error);
//       }
//     };

//     fetchNewsItem();
//   }, [id]);

//   const handleHighlight = () => {
//     const importantKeywords = [
//       /(hiệp định|thông tư|thuế|quy định|cấm|xuất khẩu|nhập khẩu)/gi,
//       /(chiến tranh)/gi,
//       /(khí hậu|biến đổi|hiệu ứng|độ ẩm|nhiệt độ|mưa|lụt|hạn hán|nóng|lạnh)/gi,
//       /(kinh tế thế giới|dự trữ|khan hiếm|giao dịch|lạm phát)/gi,
//       /(dịch bệnh)/gi,
//       /(Nhà nước)/gi,
//       /(thời tiết)/gi, // Thêm từ khóa cần highlight vào đây
//     ];

//     let content = newsItem.content;
//     const sentences = content.split('. ');

//     sentences.forEach((sentence) => {
//       importantKeywords.forEach((keyword) => {
//         if (keyword.test(sentence)) {
//           content = content.replace(
//             sentence,
//             `<span class="highlight">${sentence}</span>`
//           );
//         }
//       });
//     });

//     setHighlightedContent(content);
//   };

//   const handleSave = async () => {
//     if (!user || !newsItem) {
//       console.error('User or news item is not available');
//       return;
//     }
  
//     const saveData = {
//       user: user.id,
//       news: newsItem.id,
//     };
  
//     console.log('Save data being sent:',JSON.stringify(saveData));
  
//     try {
//       const response = await fetch('http://127.0.0.1:8000/api/save_news/', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify(saveData),
//       });
  
//       if (!response.ok) {
//         throw new Error('Failed to save news item');
//       }
  
//       console.log('News item saved successfully');
//     } catch (error) {
//       console.error('Error saving news item:', error);
//     }
//   };


//   if (!newsItem) {
//     return <div>Loading...</div>;
//   }

//   return (
//     <div className="news-detail">
//       <div>
//         <button className="highlight-btn" onClick={handleHighlight}>
//           Điểm đáng lưu ý
//         </button>
//         <button className="highlight-btn" onClick={handleSave} disabled={isSaved}>
//           {isSaved ? 'Đã Lưu' : 'Lưu'}
//         </button>
//       </div>
//       <p>{newsItem.topic}</p>
//       <h2 style={{ marginTop: '0px', marginBottom: '0px' }}>{newsItem.title}</h2>
//       <p>{newsItem.time}</p>
//       <p
//         className="content"
//         dangerouslySetInnerHTML={{ __html: highlightedContent || newsItem.content }}
//       ></p>
//       <p>{newsItem.author}</p>
//     </div>
//   );
// };

// export default NewsDetail;


// import React, { useState, useEffect } from 'react';
// import { useParams } from 'react-router-dom';
// import './NewsDetail.css'; // Import CSS

// const NewsDetail = () => {
//   const { id } = useParams();
//   const [newsItem, setNewsItem] = useState(null);
//   const [highlightedContent, setHighlightedContent] = useState('');

//   useEffect(() => {
//     const fetchNewsItem = async () => {
//       try {
//         const response = await fetch(`http://127.0.0.1:8000/api/guest/news/${id}/`);
//         if (!response.ok) {
//           throw new Error('Failed to fetch news item');
//         }
//         const data = await response.json();
//         setNewsItem(data);
//       } catch (error) {
//         console.error('Error fetching news item:', error);
//       }
//     };

//     fetchNewsItem();
//   }, [id]);

//   const handleHighlight = () => {
//     const importantKeywords = [
//       /(hiệp định|thông tư|thuế|quy định|cấm|xuất khẩu|nhập khẩu)/gi,
//       /(chiến tranh)/gi,
//       /(khí hậu|biến đổi|hiệu ứng|độ ẩm|nhiệt độ|mưa|lụt|hạn hán|nóng|lạnh)/gi,
//       /(kinh tế thế giới|dự trữ|khan hiếm|giao dịch|lạm phát)/gi,
//       /(dịch bệnh)/gi,
//       /(Nhà nước)/gi,
//       /(thời tiết)/gi, // Thêm từ khóa cần highlight vào đây
//     ];

//     let content = newsItem.content;
//     const sentences = content.split('. ');

//     sentences.forEach((sentence) => {
//       importantKeywords.forEach((keyword) => {
//         if (keyword.test(sentence)) {
//           content = content.replace(
//             sentence,
//             `<span class="highlight">${sentence}</span>`
//           );
//         }
//       });
//     });

//     setHighlightedContent(content);
//   };

//   if (!newsItem) {
//     return <div>Loading...</div>;
//   }

//   return (
//     <div className="news-detail">
//     <div>
//       <button className="highlight-btn" onClick={handleHighlight}>
//         Nguyên Nhân
//       </button>
//     </div>
//       <p>{newsItem.topic}</p>
//       <h2 style={{marginTop: '0px',marginBottom: '0px'}}>{newsItem.title}</h2>
//       <p>{newsItem.time}</p>
//       <p
//         className="content"
//         dangerouslySetInnerHTML={{ __html: highlightedContent || newsItem.content }}
//       ></p>
//       <p>{newsItem.author}</p>
//     </div>
//   );
// };

// export default NewsDetail;

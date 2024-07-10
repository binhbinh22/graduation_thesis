import React, { useState, useEffect, useContext } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { AuthContext } from '../Contexts/AuthContext';
import InfoExtractModal from './InfoExtractModal';
import saveIcon from './icons/bookmark.png';
import infoIcon from './icons/info.png';
import infoIcon1 from './icons/info.png';

import './NewsDetail.css';

const NewsDetail = () => {
  const { id } = useParams();
  const [newsItem, setNewsItem] = useState(null);
  const [highlightedContent, setHighlightedContent] = useState('');
  const [isSaved, setIsSaved] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [recommendedNews, setRecommendedNews] = useState([]);
  const { user } = useContext(AuthContext);
  const navigate = useNavigate();

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

    const fetchRecommendedNews = async () => {
      if (user && user.id) {
        const url = `http://127.0.0.1:8000/api/recommended-news/${user.id}/`;
        try {
          const response = await fetch(url);
          if (!response.ok) {
            throw new Error('Failed to fetch recommended news');
          }
          const data = await response.json();
          setRecommendedNews(data);
        } catch (error) {
          console.error('Error fetching recommended news:', error);
        }
      }
    };

    fetchNewsItem();
    fetchRecommendedNews();
  }, [id, user]);

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
        <div className="tooltip">
          <button className="action-btn" onClick={toggleModal}>
            <img src={infoIcon1} alt="Info1" />
          </button>
          <span className="tooltiptext">Các yếu tố liên quan</span>
        </div>
      </div>

      <div className="news-detail-content">
        <div className="news-detail-main">
          <p style={{ marginTop: '10px', marginBottom: '5px' }}>{newsItem.topic}</p>
          <h2 style={{ marginTop: '0px', marginBottom: '0px' }}>{newsItem.title}</h2>
          <p style={{marginTop: '0px',color:'gray'}}>{newsItem.time}</p>
          <p
            className="content"
            dangerouslySetInnerHTML={{ __html: highlightedContent || newsItem.content }}
          ></p>
          <p>{newsItem.author}</p>
        </div>
      </div>

      <div className="interested-news-section1">
        <h2>Tin tức quan tâm</h2>
        {recommendedNews.map(item => (
          <div key={item.id} className="news-link" onClick={() => navigate(`/news/${item.id}`)}>
            <div className="news-item1">
              <div className="news-item1-content" style={{ flex: 1 }}>
                <h2 style={{ margin: 0, fontSize: '1rem', fontWeight: 'bold' }}>{item.title}</h2>
              </div>
            </div>
          </div>
        ))}
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
// import InfoExtractModal from './InfoExtractModal';
// import saveIcon from './icons/bookmark.png'; 
// import infoIcon from './icons/info.png'; 
// // import starIcon from './icons/star.png'; 
// import './NewsDetail.css'; 

// const NewsDetail = () => {
//   const { id } = useParams();
//   const [newsItem, setNewsItem] = useState(null);
//   const [highlightedContent, setHighlightedContent] = useState('');
//   const [isSaved, setIsSaved] = useState(false);
//   const [showModal, setShowModal] = useState(false);
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
//       /(thời tiết)/gi,
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

//     try {
//       const response = await fetch('http://127.0.0.1:8000/api/save_news/', {
//         method: isSaved ? 'DELETE' : 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify(saveData),
//       });

//       if (!response.ok) {
//         throw new Error(`Failed to ${isSaved ? 'unsave' : 'save'} news item`);
//       }

//       setIsSaved(!isSaved);
//     } catch (error) {
//       console.error(`Error ${isSaved ? 'unsaving' : 'saving'} news item:`, error);
//     }
//   };

//   const toggleModal = () => {
//     setShowModal(!showModal);
//   };

//   if (!newsItem) {
//     return <div>Loading...</div>;
//   }

//   return (
//     <div className="news-detail-container">
//       <div className="news-detail-sidebar">
//         <div className="tooltip">
//     <button className="action-btn" onClick={handleSave}>
//       <img src={saveIcon} alt="Save" /> {isSaved ? 'Đã Lưu' : ''}
//     </button>
//     <span className="tooltiptext">Thêm vào tin tức yêu thích</span>
//   </div>
//         <div className="tooltip">
//           <button className="action-btn" onClick={toggleModal}>
//           <img src={infoIcon} alt="Info" /> 
//           </button>
//           <span className="tooltiptext">Xem thông tin quan trọng</span>
//         </div>
//         {/* <div className="tooltip">
//           <button className="action-btn" onClick={handleHighlight}>
//           <img src={starIcon} alt="Highlight" />
//           </button>
//           <span className="tooltiptext">Điểm đáng lưu ý</span>
//         </div> */}

//         {/* <button className="action-btn" onClick={toggleModal}>
//           <img src={infoIcon} alt="Info" /> 
//         </button>
//         <button className="action-btn" onClick={handleHighlight}>
//           <img src={starIcon} alt="Highlight" />
//         </button> */}
//       </div>

//       <div className="news-detail-content">
//         <p>{newsItem.topic}</p>
//         <h2 style={{ marginTop: '0px', marginBottom: '0px' }}>{newsItem.title}</h2>
//         <p>{newsItem.time}</p>
//         <p
//           className="content"
//           dangerouslySetInnerHTML={{ __html: highlightedContent || newsItem.content }}
//         ></p>
//         <p>{newsItem.author}</p>
//       </div>

//       <InfoExtractModal 
//         isOpen={showModal} 
//         onClose={toggleModal} 
//         content={newsItem.info_extrac} 
//       />
//     </div>
//   );
// };

// export default NewsDetail;




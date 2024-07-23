import React from 'react';
import shareIcon from './icons/star.png'; // Đường dẫn tới icon share

const ShareButton = ({ url }) => {
  const shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`;

  return (
    <button onClick={() => window.open(shareUrl, '_blank')}>
      <img src={shareIcon} alt="Share" />
    </button>
  );
};

export default ShareButton;

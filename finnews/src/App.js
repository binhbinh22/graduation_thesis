import React, { useContext } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './Components/Navbar';
import News from './Components/News';
import NewsPage from './Components/NewsPage';
import Save from './Components/Save';
import Highligh from './Components/Highligh';
import Header from './Components/Header';
import Footer from './Components/Footer';
import NewDetailTopic from './Components/NewDetailTopic';
import Search from './Components/Search';
import NewsDetail from './Components/NewsDetail';
import './App.css';
import Register from './Components/Register';
import Login from './Components/Login';
import { AuthProvider, AuthContext } from './Contexts/AuthContext';
import SearchResults from './Components/SearchResults';
import SelectTags from './Components/SelectTags'; 
import Recommended_news from './Components/RecommendNews';  
import User from './Components/User';
import { Chatbot } from 'react-chatbot-kit';
import config from './Components/chatbotConfig';
import 'react-chatbot-kit/build/main.css';

document.title = 'Finnews | Tin tức kinh tế';

const PrivateRoute = ({ children }) => {
  const { user } = useContext(AuthContext);
  return user ? children : <Navigate to="/" />;
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="container">
          <Header />
          <Navbar />
          <div className="news-container">
            <Routes>
              <Route path="/" element={<NewsPage />} />
              <Route path="/news" element={<News />} />
              <Route path="/topics/:topicId/news" element={<NewDetailTopic />} />
              <Route path="/save" element={<Save />} />
              <Route path="/highligh" element={<Highligh />} />
              <Route path="/news/:id" element={<NewsDetail />} />
              <Route path="/search" element={<Search />} />
              <Route path="*" element={<Navigate to="/" />} />
              <Route path="/register" element={<Register />} />
              <Route path="/recommended_news" element={<Recommended_news />} />
              <Route path="/login" element={<Login />} />
              <Route path="/user" element={<User />} />
              <Route path="/select-tags" element={
                <PrivateRoute>
                  <SelectTags />
                </PrivateRoute>
              } />
              <Route path="/search" element={<SearchResults />} />
            </Routes>
            <Chatbot config={config} />
          </div>
          <Footer />
        </div>
        {/* <Chatbot config={config} /> */}
      </Router>
    </AuthProvider>
  );
}

export default App;


// import React, { useContext } from 'react';
// import { BrowserRouter as Router, Routes, Route, Navigate, Switch } from 'react-router-dom';
// import Navbar from './Components/Navbar';
// import News from './Components/News';
// import NewsPage from './Components/NewsPage';
// import Save from './Components/Save';
// import Highligh from './Components/Highligh';
// import Header from './Components/Header';
// import Footer from './Components/Footer';
// import  NewDetailTopic from './Components/NewDetailTopic';
// import Search from './Components/Search';
// import NewsDetail from './Components/NewsDetail';
// import './App.css';
// import Register from './Components/Register';
// import Login from './Components/Login';
// import { AuthProvider,AuthContext } from './Contexts/AuthContext';
// import SearchResults from './Components/SearchResults';
// import SelectTags from './Components/SelectTags'; 
// import Recommended_news from './Components/RecommendNews';  
// import User from './Components/User';

// document.title ='Finnews | Tin tức kinh tế'

// const PrivateRoute = ({ children }) => {
//   const { user } = useContext(AuthContext);
//   return user ? children : <Navigate to="/" />;
// };

// function App() {
//   return (
//     <AuthProvider>
//     <Router>
//       <div className="container">
//         <Header />
//         <Navbar />
//         <div className="news-container">
//           <Routes>
//             <Route path="/" element={<NewsPage />} />
//             <Route path="/news" element={<News />} />
//             <Route path="/topics/:topicId/news" element={< NewDetailTopic />} />
//             <Route path="/save" element={<Save />} />
//             <Route path="/highligh" element={<Highligh />} />
//             <Route path="/news/:id" element={<NewsDetail />} />
//             <Route path="/search" element={<Search />} />
//             <Route path="*" element={<Navigate to="/" />} />
//             <Route path="/register" element={<Register/>} />
//             <Route path="/recommended_news" element={<Recommended_news/>} />
//             <Route path="/login" element={<Login/>} />
//             <Route path="/user" element={<User />} />
//             <Route path="/select-tags" element={            
//             <PrivateRoute>
//               <SelectTags />
//             </PrivateRoute>
//           } />
//             <Route path="/search" element={<SearchResults />} />
//           </Routes>
//         </div>
//         <Footer />
//       </div>
//     </Router>
//     </AuthProvider>
//   );
// }

// export default App;

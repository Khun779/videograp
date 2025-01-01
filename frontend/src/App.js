import React, { useState } from 'react';
import axios from 'axios';

const App = () => {
  const [url, setUrl] = useState('');
  const [downloading, setDownloading] = useState(false);

  const handleDownload = async () => {
    setDownloading(true);
    try {
      const response = await axios.post('http://localhost:5000/download', { url }, { responseType: 'blob' });
      const downloadUrl = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.setAttribute('download', 'video.mkv'); // or extract the original file name from response headers
      document.body.appendChild(link);
      link.click();
      link.remove();
      
      // Send a request to delete the video file from the backend
      const videoPath = response.headers['content-disposition'].split('filename=')[1];
      await axios.post('http://localhost:5000/delete', { video_path: `downloads/${videoPath}` });
    } catch (error) {
      console.error('Error downloading the video:', error);
    }
    setDownloading(false);
  };

  return (
    <div className="App">
      <h1>YouTube Video Downloader</h1>
      <input
        type="text"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        placeholder="Enter YouTube video URL"
      />
      <button onClick={handleDownload} disabled={downloading}>
        {downloading ? 'Downloading...' : 'Download'}
      </button>
    </div>
  );
};

export default App;
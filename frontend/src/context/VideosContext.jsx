import { createContext, useState } from "react";

const VideosContext = createContext();

export function VideosProvider({ children }) {
  const [videos, setVideos] = useState([]);

  return (
    <VideosContext.Provider value={{ videos, setVideos }}>
      {children}
    </VideosContext.Provider>
  );
}

export { VideosContext };

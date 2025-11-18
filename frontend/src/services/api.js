const API_BASE_URL = "http://localhost:8000/api";

export async function initiateAnalysis(url) {
  const response = await fetch(`${API_BASE_URL}/analysis`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ url }),
  });
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return await response.json();
}
//RESULT EXAMPLE
// {
//   "id": 0,
//   "url": "https://example.com/",
//   "status": "string",
//   "error_message": "string",
//   "film_id": 0
// }

//ERROR EXAMPLE
// {
//   "detail": [
//     {
//       "loc": [
//         "string",
//         0
//       ],
//       "msg": "string",
//       "type": "string"
//     }
//   ]
// }

export async function getStatus(jobId) {
  const response = await fetch(`${API_BASE_URL}/status/${jobId}`);
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return await response.json();
}

// RESULT EXAMPLE
// {
//   "id": 0,
//   "url": "https://example.com/",
//   "status": "string",
//   "error_message": "string",
//   "film_id": 0
// }
// status can be: downloading, transcribing, analyzing, complete

export async function getResult(filmId) {
  const response = await fetch(`${API_BASE_URL}/result/${filmId}`);
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  const data = await response.json();
  const now = new Date();
  const pad = (value) => value.toString().padStart(2, "0");
  return {
    ...data,
    date: `${pad(now.getDate())}.${pad(
      now.getMonth() + 1
    )}.${now.getFullYear()} ${pad(now.getHours())}:${pad(now.getMinutes())}`,
    videoTitle: "Test",
    platform: "YouTube",
  };
}
//RESULT EXAMPLE
// {
//   "url": "https://example.com/",
//   "id": 0,
//   "analysis": {
//     "battery": -1,
//     "screen": -1,
//     "memory": -1,
//     "ram_memory": -1,
//     "camera": -1,
//     "performance": -1,
//     "design": -1,
//     "quick_charge": -1,
//     "audio": -1,
//     "price": -1,
//     "id": 0,
//     "film_id": 0
//   }
// }

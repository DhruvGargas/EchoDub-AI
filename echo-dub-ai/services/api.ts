const API_BASE_URL = "http://127.0.0.1:8000";

export async function uploadVideo(file: File, language: string) {
  const formData = new FormData();

  formData.append("file", file);
  formData.append("language", language);

  const response = await fetch(`${API_BASE_URL}/upload`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(errorText);
  }

  return response.json();
}

export async function getJobStatus(jobId: string) {
  const response = await fetch(
    `${API_BASE_URL}/status/${jobId}`
  );

  if (!response.ok) {
    throw new Error("Unable to fetch status");
  }

  return response.json();
}

export function getDownloadUrl(jobId: string) {
  return `${API_BASE_URL}/download/${jobId}`;
}
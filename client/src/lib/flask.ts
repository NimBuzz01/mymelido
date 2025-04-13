export const getPrediction = async (file: File): Promise<any> => {
  const formData = new FormData();
  formData.append("audio", file);

  return fetch("http://127.0.0.1:5000/api/analyze", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      return data;
    });
};

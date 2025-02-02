import sampleData from "./sample.json";

export const getPrediction = async (
  type: "blob" | "file",
  file: Blob | File
): Promise<any> => {
  const formData = new FormData();
  if (type === "blob") {
    formData.append("audio", file, "temp_audio.webm");
  }
  if (type === "file") {
    formData.append("audio", file);
  }

  //   return fetch("http://localhost:8080/api/predict", {
  //     method: "POST",
  //     body: formData,
  //   })
  //     .then((response) => response.json())
  //     .then((data) => {
  //       return data as any;
  //     });
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(sampleData);
    }, 3000);
  });
};

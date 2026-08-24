import axios from "axios";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  "http://127.0.0.1:8000";

export async function predictBreed(imageFile) {
  const formData = new FormData();

  formData.append("image", imageFile);

  try {
    const { data } = await axios.post(
      `${API_BASE_URL}/api/v1/predict`,
      formData,
    );
    if (!data?.success || !data?.prediction?.breed || !Array.isArray(data.top_5)) {
      throw new Error("The prediction service returned an unexpected response.");
    }
    return data;
  } catch (error) {
    if (!axios.isAxiosError(error)) {
      throw error;
    }
    const status = error.response?.status;
    const detail = error.response?.data?.detail;
    const message = status >= 500
      ? "Unable to analyze the image right now. Please try again."
      : detail || "We could not process that image. Please choose another one.";
    throw new Error(
      message,
      { cause: error },
    );
  }
}

"use client";
import LoadingState from "@/components/LoadingSpinner";
import ResultsSection from "@/components/ResultsSection";
import { Button } from "@/components/ui/button";
import { FileUpload } from "@/components/ui/file-upload";
import { getPrediction } from "@/lib/flask";
import { SimilarityAnalysis } from "@/lib/result";
import { useState } from "react";
import toast from "react-hot-toast";

const Home = () => {
  const [files, setFiles] = useState<File[] | null>(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<SimilarityAnalysis | null>(null);

  const handleSubmit = async () => {
    if (!files) {
      toast.error("Please upload a file first");
      return;
    }

    try {
      setLoading(true);
      const response = await getPrediction("file", files[0]);

      if (response) {
        // const data = await response.json();
        setResults(response);
      } else {
        toast.error("Error processing file");
      }
    } catch (error) {
      console.error("Error:", error);
      toast.error("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const resetState = () => {
    setFiles(null);
    setResults(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-purple-100 to-pink-100">
      <div className="w-full max-w-[1000px] sm:px-10 px-4 mx-auto py-20">
        <h1 className="text-purple-800 mb-10 text-4xl font-semibold text-center">
          MyMelodi Copyright Analysis
        </h1>
        {loading ? (
          <LoadingState />
        ) : results ? (
          <ResultsSection results={results} />
        ) : (
          <div>
            <p className="text-xl mb-2 font-semibold max-w-xl ">
              Welcome to the MyMelodi Song Similarity Analysis tool!
            </p>
            <p className="max-w-4xl mb-10">
              This system helps you analyze the similarity between songs based
              on both their audio and lyrical content. Whether you&apos;re
              checking for potential copyright infringements or simply exploring
              musical similarities, this tool provides comprehensive results.
            </p>
            <FileUpload onChange={setFiles} />
            <div className="w-full flex">
              <Button onClick={handleSubmit} className="button mx-auto mt-10">
                Submit
              </Button>
            </div>
          </div>
        )}

        {results && (
          <div className="w-full flex">
            <Button onClick={resetState} className="button mx-auto mt-10">
              Start Again
            </Button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Home;

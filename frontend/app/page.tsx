"use client";
import { useState } from "react";
import UploadBox from "@/components/UploadBox";
import ResultCard from "@/components/ResultCard";
import { Loader2 } from "lucide-react";

interface PredictionResult {
  label: string;
  confidence: number;
}

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileSelect = (f: File) => {
    setFile(f);
    setResult(null);
    setError(null);
  };

  const handleAnalyze = async () => {
    if (!file) return;
    setLoading(true);
    setResult(null);
    setError(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/predict`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) throw new Error("Prediction failed");
      const data: PredictionResult = await res.json();
      setResult(data);
    } catch (err) {
      setError("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 flex items-center justify-center p-6">
      <div className="bg-white rounded-3xl shadow-2xl w-full max-w-lg p-8">

        <div className="text-center mb-8">
          <h1 className="text-3xl font-extrabold text-gray-800">🔍 Deepfake Detector</h1>
          <p className="text-gray-500 mt-2 text-sm">Upload a face image to check if it's real or AI-generated</p>
        </div>

        <UploadBox onFileSelect={handleFileSelect} />

        <button
          onClick={handleAnalyze}
          disabled={!file || loading}
          className={`mt-5 w-full py-3 rounded-xl font-semibold text-white transition-all
            ${!file || loading
              ? "bg-gray-300 cursor-not-allowed"
              : "bg-blue-600 hover:bg-blue-700 active:scale-95"}`}
        >
          {loading
            ? <span className="flex items-center justify-center gap-2">
                <Loader2 className="w-4 h-4 animate-spin" /> Analyzing...
              </span>
            : "Analyze Image"
          }
        </button>

        {error && (
          <p className="mt-4 text-red-500 text-center text-sm">{error}</p>
        )}

        {result && <ResultCard result={result} />}

      </div>
    </main>
  );
}
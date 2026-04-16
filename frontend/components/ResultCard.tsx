interface ResultCardProps {
  result: {
    label: string;
    confidence: number;
  };
}

export default function ResultCard({ result }: ResultCardProps) {
  const isFake = result.label === "FAKE";

  return (
    <div className={`mt-6 p-6 rounded-2xl border-2 text-center transition-all
      ${isFake ? "bg-red-50 border-red-300" : "bg-green-50 border-green-300"}`}
    >
      <div className={`text-5xl font-extrabold mb-2
        ${isFake ? "text-red-500" : "text-green-500"}`}
      >
        {isFake ? "🚨 FAKE" : "✅ REAL"}
      </div>

      <p className="text-gray-600 text-lg mt-2">
        Confidence: <span className="font-semibold">{result.confidence}%</span>
      </p>

      <div className="mt-4 w-full bg-gray-200 rounded-full h-3">
        <div
          className={`h-3 rounded-full transition-all ${isFake ? "bg-red-400" : "bg-green-400"}`}
          style={{ width: `${result.confidence}%` }}
        />
      </div>

      <p className="text-gray-400 text-sm mt-3">
        {isFake
          ? "This image shows signs of AI generation or manipulation."
          : "This image appears to be an authentic photograph."}
      </p>
    </div>
  );
}
"use client";
import { useRef, useState } from "react";
import { UploadCloud } from "lucide-react";

interface UploadBoxProps {
  onFileSelect: (file: File) => void;
}

export default function UploadBox({ onFileSelect }: UploadBoxProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragging, setDragging] = useState(false);
  const [preview, setPreview] = useState<string | null>(null);

  const handleFile = (file: File | null) => {
    if (!file || !file.type.startsWith("image/")) return;
    setPreview(URL.createObjectURL(file));
    onFileSelect(file);
  };

  return (
    <div
      onClick={() => inputRef.current?.click()}
      onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
      onDragLeave={() => setDragging(false)}
      onDrop={(e) => { e.preventDefault(); setDragging(false); handleFile(e.dataTransfer.files[0]); }}
      className={`cursor-pointer border-2 border-dashed rounded-2xl p-10 flex flex-col items-center justify-center transition-all
        ${dragging ? "border-blue-500 bg-blue-50" : "border-gray-300 bg-gray-50 hover:bg-gray-100"}`}
    >
      <input
        ref={inputRef}
        type="file"
        accept="image/*"
        className="hidden"
        onChange={(e) => handleFile(e.target.files?.[0] ?? null)}
      />

      {preview ? (
        <img src={preview} alt="preview" className="max-h-64 rounded-xl object-contain" />
      ) : (
        <>
          <UploadCloud className="w-12 h-12 text-gray-400 mb-3" />
          <p className="text-gray-600 font-medium">Drag & drop or click to upload</p>
          <p className="text-gray-400 text-sm mt-1">JPG, PNG, WEBP supported</p>
        </>
      )}
    </div>
  );
}
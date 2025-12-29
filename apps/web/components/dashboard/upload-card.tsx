"use client";

import { useRef } from "react";
import { Upload } from "lucide-react";

interface UploadCardProps {
  onFileSelect?: (file: File) => void;
  accept?: string;
}

export function UploadCard({ onFileSelect, accept = "video/*" }: UploadCardProps) {
  const inputRef = useRef<HTMLInputElement>(null);

  const handleClick = () => {
    inputRef.current?.click();
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file && onFileSelect) {
      onFileSelect(file);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    const file = e.dataTransfer.files?.[0];
    if (file && onFileSelect) {
      onFileSelect(file);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
  };

  return (
    <div
      onClick={handleClick}
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      className="group relative flex min-h-[260px] cursor-pointer flex-col items-center justify-center gap-4 rounded-xl border-2 border-dashed border-border bg-muted/30 p-6 text-center transition-all hover:border-primary hover:bg-primary/5"
    >
      <div className="flex h-14 w-14 items-center justify-center rounded-full bg-muted text-muted-foreground transition-colors group-hover:bg-primary group-hover:text-primary-foreground">
        <Upload className="h-6 w-6" />
      </div>
      <div className="space-y-1">
        <h4 className="font-bold text-foreground">Upload New Video</h4>
        <p className="text-xs text-muted-foreground">Drag & drop or click to browse</p>
      </div>
      <input
        ref={inputRef}
        type="file"
        accept={accept}
        onChange={handleChange}
        className="hidden"
        aria-label="Upload video"
      />
    </div>
  );
}

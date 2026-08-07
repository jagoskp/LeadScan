import React from "react";

interface ImagePreviewProps {
  imageUrl: string;
}

export const ImagePreview: React.FC<ImagePreviewProps> = ({ imageUrl }) => {
  return (
    <div className="p-6 bg-slate-900 border border-slate-800 rounded-xl space-y-4">
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-bold text-white">Original Document Scan</h3>
        <div className="flex gap-2">
          <button className="text-xs bg-slate-800 hover:bg-slate-700 text-slate-300 px-2 py-1 rounded">
            Zoom In
          </button>
          <button className="text-xs bg-slate-800 hover:bg-slate-700 text-slate-300 px-2 py-1 rounded">
            Rotate
          </button>
        </div>
      </div>
      <div className="aspect-[4/3] bg-slate-950 border border-slate-800 rounded-lg flex items-center justify-center text-slate-600 text-sm font-medium">
        Scan Preview Placeholder ({imageUrl})
      </div>
    </div>
  );
};
export default ImagePreview;

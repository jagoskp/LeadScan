import React from 'react';
import { Asset } from '../types/assets';

interface Props {
  asset: Asset;
}

export const ImagePreviewCanvas: React.FC<Props> = ({ asset }) => {
  return (
    <div
      style={{
        background: '#111827',
        border: '1px solid #374151',
        borderRadius: '8px',
        padding: '16px',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '220px',
        color: '#9ca3af',
      }}
    >
      <div style={{ fontSize: '3rem', marginBottom: '8px' }}>🖼️</div>
      <div style={{ fontWeight: 600, color: '#fff', fontSize: '0.95rem' }}>{asset.file_name}</div>
      <div style={{ fontSize: '0.8rem', marginTop: '4px' }}>
        Path: <code style={{ color: '#60a5fa' }}>{asset.storage_path}</code>
      </div>
      {asset.asset_metadata && (
        <div style={{ fontSize: '0.75rem', marginTop: '8px', color: '#10B981' }}>
          Dimensions: {asset.asset_metadata.width || 'N/A'} × {asset.asset_metadata.height || 'N/A'} px | DPI: {asset.asset_metadata.dpi}
        </div>
      )}
    </div>
  );
};

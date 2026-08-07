import React from 'react';
import { Asset } from '../types/assets';
import { formatFileSize } from '../utils/assetUtils';
import { AssetIntegrityBadge } from './AssetIntegrityBadge';

interface Props {
  assets: Asset[];
  selectedAssetId: string | null;
  onSelectAsset: (assetId: string) => void;
  loading: boolean;
}

export const AssetGrid: React.FC<Props> = ({ assets, selectedAssetId, onSelectAsset, loading }) => {
  if (loading) return <p style={{ color: '#9ca3af' }}>Loading Digital Assets...</p>;
  if (assets.length === 0) return <p style={{ color: '#9ca3af' }}>No digital assets stored in DAM engine.</p>;

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))', gap: '16px' }}>
      {assets.map((asset) => {
        const isSelected = asset.id === selectedAssetId;
        return (
          <div
            key={asset.id}
            onClick={() => onSelectAsset(asset.id)}
            style={{
              background: isSelected ? 'rgba(59, 130, 246, 0.15)' : '#1a1d24',
              border: isSelected ? '2px solid #3B82F6' : '1px solid #374151',
              borderRadius: '8px',
              padding: '12px',
              cursor: 'pointer',
              color: '#fff',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
            }}
          >
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                <span style={{ fontSize: '0.75rem', background: '#111827', color: '#9ca3af', padding: '2px 6px', borderRadius: '4px' }}>
                  {asset.asset_type}
                </span>
                {asset.is_immutable && (
                  <span style={{ fontSize: '0.7rem', color: '#F59E0B', fontWeight: 600 }}>🔒 Immutable</span>
                )}
              </div>
              <div style={{ fontWeight: 600, fontSize: '0.9rem', marginBottom: '4px', wordBreak: 'break-all' }}>
                🖼️ {asset.file_name}
              </div>
              <div style={{ fontSize: '0.75rem', color: '#9ca3af', marginBottom: '8px' }}>
                {formatFileSize(asset.asset_metadata?.file_size_bytes)} • {asset.asset_metadata?.color_space || 'RGB'}
              </div>
            </div>

            <div>
              <AssetIntegrityBadge integrity={asset.integrity_record} />
            </div>
          </div>
        );
      })}
    </div>
  );
};

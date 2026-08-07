import React from 'react';
import { Asset } from '../types/assets';
import { formatFileSize } from '../utils/assetUtils';
import { AssetIntegrityBadge } from './AssetIntegrityBadge';
import { AssetVersionHistory } from './AssetVersionHistory';
import { ImagePreviewCanvas } from './ImagePreviewCanvas';

interface Props {
  asset: Asset | null;
  isOpen: boolean;
  onClose: () => void;
  onVerifyIntegrity: () => void;
  onRollback: (vNum: number) => void;
}

export const AssetDetailModal: React.FC<Props> = ({
  asset,
  isOpen,
  onClose,
  onVerifyIntegrity,
  onRollback,
}) => {
  if (!isOpen || !asset) return null;

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        background: 'rgba(0,0,0,0.7)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 1000,
      }}
    >
      <div
        style={{
          background: '#1f2937',
          borderRadius: '8px',
          padding: '24px',
          maxWidth: '650px',
          width: '90%',
          color: '#fff',
          maxHeight: '90vh',
          overflowY: 'auto',
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
          <div>
            <h3 style={{ margin: 0, fontSize: '1.2rem' }}>{asset.file_name}</h3>
            <div style={{ color: '#9ca3af', fontSize: '0.8rem' }}>Asset ID: {asset.id}</div>
          </div>
          <AssetIntegrityBadge integrity={asset.integrity_record} />
        </div>

        <ImagePreviewCanvas asset={asset} />

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', margin: '16px 0' }}>
          <div style={{ background: '#111827', padding: '12px', borderRadius: '6px', fontSize: '0.85rem' }}>
            <h4 style={{ margin: '0 0 8px 0', color: '#60a5fa' }}>Asset Metadata</h4>
            <div>Size: {formatFileSize(asset.asset_metadata?.file_size_bytes)}</div>
            <div>Resolution: {asset.asset_metadata?.width} × {asset.asset_metadata?.height} px</div>
            <div>DPI: {asset.asset_metadata?.dpi}</div>
            <div>Color Space: {asset.asset_metadata?.color_space}</div>
          </div>

          <div style={{ background: '#111827', padding: '12px', borderRadius: '6px', fontSize: '0.85rem' }}>
            <h4 style={{ margin: '0 0 8px 0', color: '#60a5fa' }}>Hashes & Storage</h4>
            <div style={{ wordBreak: 'break-all' }}>SHA256: {asset.asset_metadata?.hash_sha256}</div>
            <div>MD5: {asset.asset_metadata?.checksum_md5}</div>
          </div>
        </div>

        <h4 style={{ margin: '16px 0 8px 0', color: '#60a5fa' }}>Version History</h4>
        <AssetVersionHistory versions={asset.versions} onRollback={onRollback} isImmutable={asset.is_immutable} />

        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '12px', marginTop: '20px' }}>
          <button
            onClick={onVerifyIntegrity}
            style={{ background: '#10B981', color: '#fff', border: 'none', borderRadius: '4px', padding: '8px 16px', fontWeight: 600, cursor: 'pointer' }}
          >
            🛡️ Verify Integrity
          </button>
          <button
            onClick={onClose}
            style={{ background: '#374151', color: '#fff', border: 'none', borderRadius: '4px', padding: '8px 16px', cursor: 'pointer' }}
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

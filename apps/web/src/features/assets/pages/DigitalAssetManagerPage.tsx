import React, { useState } from 'react';
import { AssetDetailModal } from '../components/AssetDetailModal';
import { AssetGrid } from '../components/AssetGrid';
import { useAssetDetail } from '../hooks/useAssetDetail';
import { useAssets } from '../hooks/useAssets';
import { assetsApi } from '../services/assetsApi';

export const DigitalAssetManagerPage: React.FC = () => {
  const { assets, assetType, setAssetType, loading, refetchAssets } = useAssets();
  const [selectedAssetId, setSelectedAssetId] = useState<string | null>(null);
  const { asset: selectedAsset, refetchAsset } = useAssetDetail(selectedAssetId);
  const [isDetailModalOpen, setIsDetailModalOpen] = useState<boolean>(false);

  const handleSelectAsset = (assetId: string) => {
    setSelectedAssetId(assetId);
    setIsDetailModalOpen(true);
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) return;
    const file = e.target.files[0];
    try {
      await assetsApi.uploadAsset(file, 'original_scan', true);
      await refetchAssets();
    } catch (err) {
      console.error('Upload failed', err);
    }
  };

  const handleVerifyIntegrity = async () => {
    if (!selectedAssetId) return;
    try {
      await assetsApi.verifyIntegrity(selectedAssetId);
      await refetchAsset();
    } catch (err) {
      console.error('Integrity check failed', err);
    }
  };

  const handleRollback = async (versionNumber: number) => {
    if (!selectedAssetId) return;
    try {
      await assetsApi.rollbackVersion(selectedAssetId, versionNumber);
      await refetchAsset();
    } catch (err) {
      console.error('Rollback failed', err);
    }
  };

  return (
    <div
      style={{
        padding: '32px',
        background: '#0f1117',
        minHeight: '100vh',
        color: '#fff',
        fontFamily: 'Inter, system-ui, sans-serif',
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <div>
          <h1 style={{ margin: 0, fontSize: '1.8rem', fontWeight: 800 }}>Digital Asset Management (DAM) Engine</h1>
          <p style={{ color: '#9ca3af', fontSize: '0.95rem', marginTop: '4px' }}>
            Single Source of Truth for Original Images, Company Logos, Thumbnails & Derivative Previews.
          </p>
        </div>

        <label
          style={{
            background: '#3B82F6',
            color: '#fff',
            padding: '10px 20px',
            borderRadius: '6px',
            fontWeight: 700,
            cursor: 'pointer',
          }}
        >
          📤 Upload Asset
          <input type="file" onChange={handleFileUpload} style={{ display: 'none' }} />
        </label>
      </div>

      <div style={{ display: 'flex', gap: '12px', marginBottom: '20px' }}>
        <button
          onClick={() => setAssetType(undefined)}
          style={{
            background: !assetType ? '#3B82F6' : '#1a1d24',
            color: '#fff',
            border: 'none',
            borderRadius: '6px',
            padding: '8px 16px',
            cursor: 'pointer',
          }}
        >
          All Assets
        </button>
        <button
          onClick={() => setAssetType('original_scan')}
          style={{
            background: assetType === 'original_scan' ? '#3B82F6' : '#1a1d24',
            color: '#fff',
            border: 'none',
            borderRadius: '6px',
            padding: '8px 16px',
            cursor: 'pointer',
          }}
        >
          Immutable Scan Images
        </button>
        <button
          onClick={() => setAssetType('company_logo')}
          style={{
            background: assetType === 'company_logo' ? '#3B82F6' : '#1a1d24',
            color: '#fff',
            border: 'none',
            borderRadius: '6px',
            padding: '8px 16px',
            cursor: 'pointer',
          }}
        >
          Company Logos
        </button>
      </div>

      <AssetGrid
        assets={assets}
        selectedAssetId={selectedAssetId}
        onSelectAsset={handleSelectAsset}
        loading={loading}
      />

      <AssetDetailModal
        asset={selectedAsset}
        isOpen={isDetailModalOpen}
        onClose={() => setIsDetailModalOpen(false)}
        onVerifyIntegrity={handleVerifyIntegrity}
        onRollback={handleRollback}
      />
    </div>
  );
};

export default DigitalAssetManagerPage;

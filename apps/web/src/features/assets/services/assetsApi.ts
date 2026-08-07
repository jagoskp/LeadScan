import { Asset, AssetIntegrity, CompanyLogo } from '../types/assets';

const BASE_URL = '/api/v1/assets';

export const assetsApi = {
  async listAssets(assetType?: string, leadId?: string): Promise<Asset[]> {
    const params = new URLSearchParams();
    if (assetType) params.append('asset_type', assetType);
    if (leadId) params.append('lead_id', leadId);

    const res = await fetch(`${BASE_URL}?${params.toString()}`);
    if (!res.ok) throw new Error('Failed to fetch digital assets');
    return res.json();
  },

  async getAsset(assetId: string): Promise<Asset> {
    const res = await fetch(`${BASE_URL}/${assetId}`);
    if (!res.ok) throw new Error('Failed to fetch asset details');
    return res.json();
  },

  async uploadAsset(file: File, assetType: string = 'original_scan', isImmutable: boolean = false): Promise<Asset> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('asset_type', assetType);
    formData.append('is_immutable', isImmutable ? 'true' : 'false');

    const res = await fetch(`${BASE_URL}/upload`, {
      method: 'POST',
      body: formData,
    });
    if (!res.ok) throw new Error('Asset upload failed');
    return res.json();
  },

  async verifyIntegrity(assetId: string): Promise<AssetIntegrity> {
    const res = await fetch(`${BASE_URL}/${assetId}/verify-integrity`, { method: 'POST' });
    if (!res.ok) throw new Error('Integrity verification failed');
    return res.json();
  },

  async rollbackVersion(assetId: string, versionNumber: number): Promise<Asset> {
    const res = await fetch(`${BASE_URL}/${assetId}/rollback?version_number=${versionNumber}`, { method: 'POST' });
    if (!res.ok) throw new Error('Version rollback failed');
    return res.json();
  },

  async getCompanyLogo(companyId: string): Promise<CompanyLogo> {
    const res = await fetch(`${BASE_URL}/company-logo/${companyId}`);
    if (!res.ok) throw new Error('Failed to fetch company logo');
    return res.json();
  },
};

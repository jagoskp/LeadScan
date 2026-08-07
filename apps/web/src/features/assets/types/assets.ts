export interface AssetMetadata {
  id: string;
  file_size_bytes: number;
  width?: number;
  height?: number;
  dpi?: string;
  color_space?: string;
  hash_sha256: string;
  checksum_md5?: string;
}

export interface AssetIntegrity {
  id: string;
  expected_hash: string;
  actual_hash?: string;
  integrity_status: string;
  last_checked_at: string;
}

export interface AssetVersion {
  id: string;
  asset_id: string;
  version_number: number;
  storage_path: string;
  checksum_sha256: string;
  created_at: string;
}

export interface AssetThumbnail {
  id: string;
  thumbnail_type: string;
  width: number;
  height: number;
  storage_path: string;
}

export interface Asset {
  id: string;
  lead_id?: string;
  company_id?: string;
  contact_id?: string;
  review_session_id?: string;
  ocr_result_id?: string;
  owner_id?: string;
  asset_type: string;
  file_name: string;
  storage_path: string;
  mime_type: string;
  is_immutable: boolean;
  created_at: string;
  updated_at: string;
  asset_metadata?: AssetMetadata;
  integrity_record?: AssetIntegrity;
  versions: AssetVersion[];
  thumbnails: AssetThumbnail[];
}

export interface CompanyLogo {
  id: string;
  company_id: string;
  asset_id?: string;
  is_default: boolean;
  logo_url: string;
  created_at: string;
}

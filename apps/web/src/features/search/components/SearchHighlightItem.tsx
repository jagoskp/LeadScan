import React from 'react';
import { SearchResultItem } from '../types/search';
import { formatScoreBadge } from '../utils/searchUtils';

interface Props {
  item: SearchResultItem;
}

export const SearchHighlightItem: React.FC<Props> = ({ item }) => {
  return (
    <div
      style={{
        background: '#1a1d24',
        border: '1px solid #374151',
        borderRadius: '8px',
        padding: '16px',
        marginBottom: '12px',
        color: '#fff',
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '6px' }}>
        <div>
          <span style={{ fontSize: '0.8rem', color: '#9ca3af', textTransform: 'uppercase', marginRight: '8px' }}>
            [{item.source_type}]
          </span>
          <strong style={{ fontSize: '1.1rem', color: '#60a5fa' }}>{item.title}</strong>
        </div>
        <div style={{ background: 'rgba(59, 130, 246, 0.2)', color: '#60a5fa', padding: '2px 8px', borderRadius: '4px', fontSize: '0.8rem', fontWeight: 600 }}>
          {formatScoreBadge(item.score)} ({item.score.toFixed(1)})
        </div>
      </div>

      <div style={{ fontSize: '0.85rem', color: '#d1d5db', marginBottom: '8px' }}>
        {item.company_name && <span>🏢 <strong>Company:</strong> {item.company_name} &nbsp;&nbsp;</span>}
        {item.gst_number && <span>📑 <strong>GST:</strong> {item.gst_number} &nbsp;&nbsp;</span>}
        {item.email && <span>📧 <strong>Email:</strong> {item.email} &nbsp;&nbsp;</span>}
        {item.phone && <span>📞 <strong>Phone:</strong> {item.phone}</span>}
      </div>

      <div style={{ background: '#111827', padding: '8px 12px', borderRadius: '4px', fontSize: '0.8rem', color: '#10B981', borderLeft: '3px solid #10B981' }}>
        {item.highlighted_match}
      </div>
    </div>
  );
};
